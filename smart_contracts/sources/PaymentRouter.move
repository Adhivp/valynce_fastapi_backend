module addr::PaymentRouter {
    use aptos_framework::coin;
    use aptos_framework::aptos_coin;

    struct DatasetPrice has key {
        dataset_id: u64,
        base_price: u64,
        per_query_price: u64,
    }

    public entry fun set_price(
        account: &signer,
        dataset_id: u64,
        base_price: u64,
        per_query_price: u64
    ) {
        move_to(account, DatasetPrice {
            dataset_id,
            base_price,
            per_query_price
        });
    }

    public entry fun pay_for_license(
        buyer: &signer,
        seller: address,
        dataset_id: u64
    ) acquires DatasetPrice {
        let price = borrow_global<DatasetPrice>(seller);
        coin::transfer<aptos_coin::AptosCoin>(
            buyer,
            seller,
            price.base_price
        );
    }

    public entry fun pay_per_query(
        buyer: &signer,
        seller: address,
        dataset_id: u64
    ) acquires DatasetPrice {
        let price = borrow_global<DatasetPrice>(seller);
        coin::transfer<aptos_coin::AptosCoin>(
            buyer,
            seller,
            price.per_query_price
        );
    }
}

module addr::Royalties {
    use aptos_framework::coin;
    use aptos_framework::aptos_coin;
    use std::signer;
    use std::vector;

    struct RoyaltyConfig has key {
        dataset_id: u64,
        main_owner: address,
        contributors: vector<address>,
        share: u64, // percentage for contributors
    }

    public entry fun set_royalty(
        account: &signer,
        dataset_id: u64,
        contributors: vector<address>,
        share: u64
    ) {
        move_to(account, RoyaltyConfig {
            dataset_id,
            main_owner: signer::address_of(account),
            contributors,
            share,
        });
    }

    public entry fun distribute(
        payer: &signer,
        dataset_id: u64,
        amount: u64
    ) acquires RoyaltyConfig {
        let payer_addr = signer::address_of(payer);
        let config = borrow_global<RoyaltyConfig>(payer_addr);

        let share_amount = amount * config.share / 100;
        let main_amount = amount - share_amount;

        // Main owner
        coin::transfer<aptos_coin::AptosCoin>(
            payer,
            config.main_owner,
            main_amount
        );

        // Split among contributors
        let num = vector::length(&config.contributors);
        let indiv = share_amount / num;

        let i = 0;
        while (i < num) {
            let contrib = *vector::borrow(&config.contributors, i);
            coin::transfer<aptos_coin::AptosCoin>(payer, contrib, indiv);
            i = i + 1;
        };
    }
}

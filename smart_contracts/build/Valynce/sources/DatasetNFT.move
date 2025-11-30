module addr::DatasetNFT {

    use aptos_framework::timestamp;
    use aptos_framework::event;
    use aptos_framework::account;
    use aptos_std::string;
    use std::signer;

    struct Dataset has key {
        id: u64,
        owner: address,
        hash: string::String,
        uri: string::String,
        created_at: u64,
    }

    struct DatasetMintEvent has drop, store {
        id: u64,
        owner: address,
        hash: string::String,
    }

    struct Events has key {
        dataset_minted: event::EventHandle<DatasetMintEvent>,
    }

    /// Initialize event store
    public entry fun init(acc: &signer) {
        move_to(acc, Events {
            dataset_minted: account::new_event_handle<DatasetMintEvent>(acc)
        });
    }

    /// Mint a dataset NFT
    public entry fun mint_dataset(
        creator: &signer,
        id: u64,
        hash: string::String,
        uri: string::String
    ) {

        let owner = signer::address_of(creator);

        let ds = Dataset {
            id,
            owner,
            hash,
            uri,
            created_at: timestamp::now_seconds(),
        };

        move_to(creator, ds);

        let events = borrow_global_mut<Events>(owner);
        event::emit_event(&mut events.dataset_minted, DatasetMintEvent {
            id,
            owner,
            hash,
        });
    }

    #[view]
    public fun get_dataset_id(owner: address): u64 acquires Dataset {
        borrow_global<Dataset>(owner).id
    }

    #[view]
    public fun get_dataset_hash(owner: address): string::String acquires Dataset {
        borrow_global<Dataset>(owner).hash
    }

}

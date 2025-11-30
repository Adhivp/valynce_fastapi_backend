module addr::Licensing {

    use aptos_framework::timestamp;

    struct License has key {
        dataset_id: u64,
        user: address,
        expires_at: u64,
        license_type: u8, // 0 = unlimited, 1 = time-based, 2 = per-query
    }

    public entry fun grant_license(
        account: &signer,
        dataset_id: u64,
        user: address,
        duration_secs: u64,
        license_type: u8
    ) {
        let expiry = timestamp::now_seconds() + duration_secs;

        move_to(account, License {
            dataset_id,
            user,
            expires_at: expiry,
            license_type
        });
    }

    public fun has_access(user: address, dataset_id: u64): bool acquires License {
        if (!exists<License>(user)) return false;
        let lic = borrow_global<License>(user);
        lic.dataset_id == dataset_id && timestamp::now_seconds() < lic.expires_at
    }
}

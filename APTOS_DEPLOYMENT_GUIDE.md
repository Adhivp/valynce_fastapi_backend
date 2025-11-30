# 🚀 Aptos Smart Contracts Deployment Guide

This guide will walk you through deploying the Valynce smart contracts to Aptos testnet.

## 📋 Prerequisites

1. **Install Aptos CLI**
   ```bash
   # macOS
   brew install aptos
   
   # Or download from: https://aptos.dev/tools/install-cli/
   ```

2. **Verify Installation**
   ```bash
   aptos --version
   ```

## 🔑 Step 1: Create Aptos Account & Get Testnet Tokens

### 1.1 Initialize Aptos CLI
```bash
cd valynce_fastapi_backend/smart_contracts
aptos init
```

When prompted:
- Choose network: `testnet`
- Press Enter to generate a new account
- Save the private key shown!

### 1.2 Your Account Information
After initialization, you'll see:
```
Account created successfully!
Account Address: 0x1234...abcd
Private Key: 0xabcd...1234
```

**⚠️ IMPORTANT: Save your private key securely!**

### 1.3 Find Your Account Address
```bash
# Your account info is stored in .aptos/config.yaml
cat .aptos/config.yaml
```

Copy your account address (starts with `0x`)

### 1.4 Get Testnet Tokens
Visit the Aptos Faucet:
- **Web Faucet**: https://aptoslabs.com/testnet-faucet
- Enter your account address
- Request 1 APT (1 APT = 100,000,000 Octas)

Or use CLI:
```bash
aptos account fund-with-faucet --account YOUR_ADDRESS
```

### 1.5 Check Your Balance
```bash
aptos account list --account YOUR_ADDRESS
```

## 📝 Step 2: Configure Move.toml

Edit `smart_contracts/Move.toml` and replace `addr = "_"` with your account address:

```toml
[addresses]
addr = "0xYOUR_ACCOUNT_ADDRESS_HERE"
```

Example:
```toml
[addresses]
addr = "0x123456789abcdef123456789abcdef123456789abcdef123456789abcdef1234"
```

## 🔨 Step 3: Compile Smart Contracts

```bash
cd smart_contracts
aptos move compile
```

Expected output:
```
Compiling, may take a little while to download git dependencies...
INCLUDING DEPENDENCY AptosFramework
BUILDING Valynce
Success!
```

## 🚀 Step 4: Deploy to Testnet

```bash
aptos move publish --named-addresses addr=YOUR_ADDRESS
```

When prompted:
- Type `yes` to confirm
- Wait for deployment (30-60 seconds)

Expected output:
```
Transaction submitted: 0xTRANSACTION_HASH
{
  "Result": {
    "transaction_hash": "0x...",
    "gas_used": 1234,
    "success": true,
    "vm_status": "Executed successfully"
  }
}
```

## ✅ Step 5: Verify Deployment

### 5.1 Check on Aptos Explorer
Visit: https://explorer.aptoslabs.com/?network=testnet

Search for your account address to see deployed modules:
- DatasetNFT
- Licensing
- PaymentRouter
- Royalties

### 5.2 Verify with CLI
```bash
aptos account list --account YOUR_ADDRESS
```

## 🔧 Step 6: Update Backend Configuration

Update your `.env` file:

```env
APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1
APTOS_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
APTOS_CONTRACT_ADDRESS=0xYOUR_ACCOUNT_ADDRESS
```

## 🧪 Step 7: Test the Integration

### 7.1 Start FastAPI Server
```bash
cd ..
source valynce_venv/bin/activate
python main.py
```

### 7.2 Test Endpoints
Visit: http://localhost:8000/docs

Test these endpoints:
1. `GET /aptos/` - Check Aptos service info
2. `POST /aptos/account/create` - Create new account
3. `POST /aptos/account/fund` - Fund account from faucet
4. `GET /aptos/account/balance/{address}` - Check balance
5. `POST /aptos/dataset/mint` - Mint a dataset NFT

### 7.3 Example: Create Account
```bash
curl -X POST http://localhost:8000/aptos/account/create
```

Response:
```json
{
  "address": "0x...",
  "private_key": "0x...",
  "public_key": "0x...",
  "message": "Account created successfully. Save your private key securely!"
}
```

### 7.4 Example: Fund Account
```bash
curl -X POST http://localhost:8000/aptos/account/fund \
  -H "Content-Type: application/json" \
  -d '{"address": "0xYOUR_ADDRESS", "amount": 100000000}'
```

### 7.5 Example: Mint Dataset NFT
```bash
curl -X POST http://localhost:8000/aptos/dataset/mint \
  -H "Content-Type: application/json" \
  -d '{
    "private_key": "0xYOUR_PRIVATE_KEY",
    "dataset_id": 1,
    "hash": "QmXYZ123...",
    "uri": "ipfs://QmXYZ123..."
  }'
```

## 📚 Common Commands Reference

### Account Management
```bash
# Create new account
aptos init --profile PROFILE_NAME

# Check balance
aptos account list --account ADDRESS

# Get testnet tokens
aptos account fund-with-faucet --account ADDRESS

# Transfer tokens
aptos account transfer --account ADDRESS --amount AMOUNT
```

### Contract Operations
```bash
# Compile contracts
aptos move compile

# Run tests
aptos move test

# Publish/Deploy
aptos move publish --named-addresses addr=YOUR_ADDRESS

# Run a function
aptos move run --function-id ADDRESS::MODULE::FUNCTION
```

### View Resources
```bash
# View all resources in account
aptos account list --account ADDRESS

# View specific resource
aptos move view --function-id ADDRESS::MODULE::VIEW_FUNCTION
```

## 🔍 Useful Links

- **Aptos Testnet Faucet**: https://aptoslabs.com/testnet-faucet
- **Aptos Explorer**: https://explorer.aptoslabs.com/?network=testnet
- **Aptos Documentation**: https://aptos.dev
- **Move Language Docs**: https://move-language.github.io/move/
- **Aptos SDK Python**: https://aptos.dev/sdks/python-sdk/

## 🐛 Troubleshooting

### Error: Account doesn't exist
- Make sure you funded your account from the faucet
- Check balance: `aptos account list --account ADDRESS`

### Error: Insufficient gas
- Request more tokens from faucet
- Each deployment needs ~0.01 APT

### Error: Module already published
- You can only publish once per address
- Create a new account to redeploy

### Error: Compilation failed
- Check `Move.toml` has correct account address
- Ensure all dependencies are downloaded

## 🎯 Next Steps

1. ✅ Deploy contracts to testnet
2. ✅ Test all endpoints via Swagger UI
3. ✅ Create datasets and mint NFTs
4. ✅ Test licensing and payment flows
5. ✅ Set up royalty distribution
6. 🚀 Deploy to mainnet (when ready)

## 💡 Pro Tips

1. **Always test on testnet first**
2. **Keep your private keys secure** - never commit to git
3. **Use .gitignore** for `.aptos/` folder
4. **Document your contract addresses** after deployment
5. **Monitor gas usage** on testnet before mainnet
6. **Use multiple test accounts** for end-to-end testing

## 📞 Support

If you encounter issues:
1. Check Aptos Discord: https://discord.gg/aptoslabs
2. Read the docs: https://aptos.dev
3. Check your account balance and network status

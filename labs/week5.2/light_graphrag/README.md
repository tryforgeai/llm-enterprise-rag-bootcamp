Follow instructions from https://github.com/HKUDS/LightRAG
use the sample_env for .env

```bash
curl -fsSL https://bun.com/install | bash
# restart terminal so bun becomes available
git clone https://github.com/HKUDS/LightRAG.git
uv tool install "lightrag-hku[api]"
cd LightRAG/lightrag_webui
bun install --frozen-lockfile
bun run build
cd ..
```

If you want to reset run the following:
```bash
rm -rf rag_storage/
```

Then to set the environment:
```bash
cp ../sample_env .env
```
Note: update accordingly as per the instruction(comments) in the .env file

To run the LightRAG server:
```bash
lightrag-server
```
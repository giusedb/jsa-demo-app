pushd client
npm run dev &
popd

pushd server
poetry run python main.py web blacksheep --debug
popd


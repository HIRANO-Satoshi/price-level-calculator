# patch generated runtime.ts and yarn install and yarn link

pushd ../luncho-typescript-fetch
# export type FetchAPI = GlobalFetch['fetch'];
#  ->
#    export type FetchAPI = typeof fetch;
if [ ! -e runtime.ts.org ]; then
    mv runtime.ts runtime.ts.org
fi
sed -e "s/GlobalFetch\['fetch'\]/typeof fetch/" src/runtime.ts.org >src/runtime.ts
yarn install
yarn link
popd


pushd ../app
yarn link "luncho-typescript-fetch"
popd

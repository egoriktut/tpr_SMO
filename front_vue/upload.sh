#!/bin/bash

npm run build

source_dir="dist/assets"
target_dir="../static"

mv "$source_dir"/index-*.js "$source_dir/index.js"
cp "$source_dir/index.js" "$target_dir"
echo "copied index.js"

mv "$source_dir"/index-*.css "$source_dir/index.css"
cp "$source_dir/index.css" "$target_dir"

echo "copied index.css"
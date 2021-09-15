if [ -d '$./docs' ]; then
    rmdir ./docs
fi

if [ -d '$./html' ]; then
    rmdir ./html
fi

mv ./html/aiobungie ./docs
mv ./html/** ./docs
rmdir ./html

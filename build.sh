# zips the scr and package directories into a zip file for upload to aws lambda
echo "Building the deployment package"

echo "Installing dependencies..."
if [ -d ".temp" ]; then
    rm -r .temp
fi
mkdir .temp
pip3 install ./library --target ./.temp --quiet

echo "Zipping files..."
mkdir -p build
now=$(date +"%Y-%m-%d_%H-%M-%S")
cd lambda
zip -rq ../build/deploy-$now.zip .
cd ..

cd .temp
zip -rq ../build/deploy-$now.zip .
cd ..

echo "Cleaning up..."
rm -r .temp

echo "Done! Deployment package created at build/deploy-$now.zip"
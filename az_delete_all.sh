# Get a list of all resource groups
rgs=$(az group list --query "[].name" -o tsv)

# Loop through each resource group and delete it
for rg in $rgs
do
    echo "Deleting resource group: $rg"
    az group delete --name $rg --yes --no-wait
done
#!/bin/bash

# script to delete all resource groups in a subscription using Azure CLI

# get the current subscription name to confirm
subscription=$(az account show --query name -o tsv)

echo "Use this script with caution!"
echo "You are about to delete all resource groups in the subscription: $subscription"

# prompt for confirmation
read -p "Are you sure? (y/n) " will_delete

if [[ $will_delete == [Yy]* ]]; then
	echo "Deleting resource groups..."

	groups=$(az group list --query "[].name" -o tsv)

	# Loop through each group name and delete it
	for group in $groups; do
		az group delete --name "$group" --yes
	done

	echo "All resource groups have been deleted."
	exit 0
fi

echo "Exiting without deleting any resource groups."
echo "Probably wise."

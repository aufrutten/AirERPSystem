#!/bin/sh

script_dir=$(dirname "$0")

public_env_temp="${script_dir}/env_templates/public.env.tmp"
private_env_temp="${script_dir}/env_templates/private.env.tmp"

parent_dir="${script_dir}/../"

if [[ ! -e "${parent_dir}public.env" ]]; then
    cp "${public_env_temp}" "${parent_dir}public.env"
    echo "The public env were successfully copied."
else
    echo "The public env files already exist."
fi

if [[ ! -e "${parent_dir}private.env" ]]; then
    cp "${private_env_temp}" "${parent_dir}private.env"
    echo "The private env were successfully copied."
else
    echo "The private env files already exist."
fi

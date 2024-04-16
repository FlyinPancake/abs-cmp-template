default:
    just --choose

dev:
    #!/bin/sh
    cd {{justfile_directory()}}/custom_metadata_provider
    uvicorn main:app --reload
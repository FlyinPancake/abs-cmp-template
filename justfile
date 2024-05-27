default:
    just --choose

dev:
    #!/bin/sh
    cd {{justfile_directory()}}/custom_metadata_provider
    fastapi dev

run:
    #!/bin/sh
    cd {{justfile_directory()}}/custom_metadata_provider
    fastapi run
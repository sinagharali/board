# Project Name

Board (THIS PROJECT IS STILL UNDER DEVELOPMENT.)

## Introduction

This project is just to test my knowledge to implement something hard and production ready.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Authorization](#Authorization)
  - [The most important features](#The-most-important-feature)
  - [DSL Authorization Model](#DSL-Authorization-Model)
  - [Interaction with OpenFGA API](#Interaction-with-OpenFGA-API)

## Installation

Follow these steps to set up the project:

1. Create a Python environment

   ```bash
   python -m venv venv
   venv\Scripts\activate      # For Windows
   ```

2. Install Python dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the project using Docker Compose**

   ```bash
   docker-compose up -d
   ```

4. **Set up your database **

   - I used postgersql for this project, just setup and migrate. its either a dcoker container or pgadmin.

5. **Environment variables**
   Create a `.env` file in the project root with the following variables:

   ```env
    DATABASE_URL=postgresql+asyncpg://your_db_user:your_db_password@localhost/your_db_name
    DATABASE_FUTURE=True # SET False FOR PROD
    DATABASE_ECHO=True
    DATABASE_HIDE_PARAMETERS=False # SET True FOR PROD

    AUTH_ACCESS_TOKEN_SECRET_KEY=your_access_token_secret_key
    AUTH_REFRESH_TOKEN_SECRET_KEY=your_refresh_token_secret_key
    AUTH_ALG=HS256
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=15
    AUTH_REFRESH_TOKEN_EXPIRE_DAYS=7

    SESSION_EXPIRE_DAYS=7

    ENV=dev
    LOG_TOKEN=your_log_token
    LOG_HOST=your_log_host

    FGA_API_URL=http://localhost:8080
    FGA_STORE_ID=your_fga_store_id
    FGA_MODEL_ID=your_fga_model_id

   ```

   - Replace `your_*` with your actual values.

6. **Verify the setup**

   - Check that all services are running:

     ```bash
     docker-compose ps
     ```

   - Run migrations (if applicable):

     ```bash
     alembic upgrade head
     ```

## Authorization

I use openfga for this project, They did a greate job to make this engine and im greatful i use it for this project

For authorization model design based on the tutoial the openfga recommend (the web site: https://openfga.dev/docs/modeling/getting-started) :

### The most important feature:

#### Board Features

- A user can perform the action create on a board if they are authenticated.

- A user becomes the owner of the board after creating it.

- A user can perform the action change ownership on a board if they are the owner of the board.

- A user can perform the action change information on a board if they are the owner of the board or they are an admin with change_info permission.

- A user can perform the action invite users to a board if they are the owner or an admin with invite_users permission.

- A user can perform the action add admins to a board if they are the owner or an admin with add_admins permission.

- A user can perform the action remove a member from a board if they are the owner or an admin with remove_member permission.

- A user can perform the action remove an admin from a board if they are the owner.

- A user can perform the action view a board if they are the owner or a member of the board.

- A user can perform the action join a board if they are invited to the board.

- A user can perform the action become a member of a board after joining or being added by an owner/admin.

- A user can perform the action become an admin if they are explicitly assigned admin by the owner.

- A user can perform the action create a note in a board if they are a member or the owner of the board.

#### Note Features

- A user can perform the action view a note if they have permission to view the board the note belongs to.

- A user can perform the action edit a note if they are the creator of the note or have manage_notes permission on the board.

- A user can perform the action delete a note if they are the creator of the note or have manage_notes permission on the board.

- A user becomes the creator of a note when they create it, and must be a member of the board.

### DSL Authorization Model:

This is the output based on the MVP, later maybe I add some features, but for now that's enough.

```DSL
model
  schema 1.1

type user

type board
  relations
    define owner: [user]
    define change_ownership: owner

    define admin: [user] and member
    define remove_member: ([user] and admin) or owner

    define remove_admin: owner

    define member: [user]
    define view: owner or member

    define invited: [user]
    define join: invited

    define can_create_note: member or owner

    define change_info: ([user] and admin) or owner
    define manage_notes: ([user] and admin) or owner
    define invite_users: ([user] and admin) or owner
    define add_admins: ([user] and admin) or owner

type note
  relations
    define board: [board]
    define creator: [user] and member from board

    define can_view: view from board
    define can_edit : creator or manage_notes from board
    define can_delete : creator or manage_notes from board
```

### Interaction with OpenFGA API

based on the python sdk and the github page, they said :

> We strongly recommend you initialize the OpenFgaClient only once and then re-use it throughout your app, otherwise you will incur the cost of having to re-initialize multiple times or at every request, the cost of reduced connection pooling and re-use, and would be particularly costly in the client credentials flow, as that flow will be preformed on every request.

and based on this info, for the client, I use singleton design pattern as you can see here:

```py
class OpenFgaClientSingleton:
    _instance: OpenFgaClient = None

    @classmethod
    async def get_instance(cls) -> OpenFgaClient:
        if cls._instance is None:
            config = ClientConfiguration(
                api_url=acl_settings.api_url,
                store_id=acl_settings.store_id,
                authorization_model_id=acl_settings.model_id,
            )

            cls._instance = await OpenFgaClient(config).__aenter__()
        return cls._instance

    @classmethod
    async def close(cls):  # Dont forget to Close when the app lifetime end.
        if cls._instance:
            await cls._instance.__aexit__(None, None, None)
            cls._instance = None
```

I used "No Credentials" client for local development but I strongly suggest to use "Client Credentials" for production.

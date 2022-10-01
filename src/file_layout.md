
## File Layout
.
├── projects
│   ├── apis                       # API Controllers
│   │   ├── cart.py                # Cart API controller
│   │   └── account.py             # Account API controller
│   ├── api_specs                  # API spec define (Swagger)
│   │   ├── account.yml            # Login API spec
│   │   ├── cart_add.yml           # Cart add API spec
│   │   └── cart_checkout.yml      # Cart checkout API spec
│   ├── db                         # DB
│   │   ├── client.py              # DB client
│   │   ├── mode.py                # DB schema
│   │   └──ops.py                 # DB operations
│   ├── helper                     # DB
│   │   ├── logics.py              # Bussiness Logics
│   │   └── utils.py               # utilities
│   ├── app.py                     # Server entry
│   ├── configs.py                 # Server Configs (Production/Testing)
│   ├── init_db.py                 # Create demo user and products
│   ├── tests                      # Unit tests
│   │   ├── __init__.py            # TestCase class define
│   │   ├── test_api_account.py    # Account API tests
│   │   ├── test_api_cart.py       # Cart API tests
│   │   ├── test_db_client.py      # DB client tests
│   │   ├── test_db_ops.py         # DB operations tests
│   │   ├── test_helper_logics.py  # Bussiness logics tests
│   │   └──test_helper_utils.py    # Custom classes tests
├── requirements.txt               # Python packages requirements
├── Dockerfile                     # Docker image build recipe
└── README.md                      # Documentation

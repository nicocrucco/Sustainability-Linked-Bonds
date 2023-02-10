import pytest
from algosdk import account
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.transaction import PaymentTxn
from algosdk.v2client.algod import AlgodClient

from beaker import sandbox
from beaker.consts import algo

ACCOUNT_FUNDS = 10 * algo


class Account(AccountTransactionSigner):
    def __init__(self, private_key: str):
        super().__init__(private_key)
        self.address = account.address_from_private_key(self.private_key)

    algod_client = sandbox.get_algod_client()


@pytest.fixture(scope="module")
def algod_client() -> AlgodClient:
    return sandbox.get_algod_client()


@pytest.fixture(scope="class")
def sandbox_faucet() -> Account:
    faucet = sandbox.get_accounts().pop()
    return Account(private_key=faucet.private_key)


@pytest.fixture(scope="class")
def issuer(sandbox_faucet: Account) -> Account:
    private_key, _ = account.generate_account()
    issuer = Account(private_key=private_key)
    sandbox.add_account(issuer.private_key)
    sp = sandbox_faucet.algod_client.suggested_params()
    fund_txn = PaymentTxn(
        sender=sandbox_faucet.address,
        sp=sp,
        receiver=issuer.address,
        amt=ACCOUNT_FUNDS,
    )
    sandbox_faucet.algod_client.send_transaction(
        fund_txn.sign(sandbox_faucet.private_key)
    )
    return issuer


@pytest.fixture(scope="class")
def investor(sandbox_faucet: Account) -> Account:
    private_key, _ = account.generate_account()
    investor = Account(private_key=private_key)
    sandbox.add_account(investor.private_key)
    sp = sandbox_faucet.algod_client.suggested_params()
    fund_txn = PaymentTxn(
        sender=sandbox_faucet.address,
        sp=sp,
        receiver=investor.address,
        amt=ACCOUNT_FUNDS,
    )
    sandbox_faucet.algod_client.send_transaction(
        fund_txn.sign(sandbox_faucet.private_key)
    )
    return investor

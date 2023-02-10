from algosdk.transaction import PaymentTxn


class TestSLBCreate:
    def test_happy_path(self, issuer) -> None:
        print(f"Issuer Account: {issuer.address}")
        sp = issuer.algod_client.suggested_params()
        test_txn = PaymentTxn(
            sender=issuer.address,
            sp=sp,
            receiver=issuer.address,
            amt=0,
        )

        issuer.algod_client.send_transaction(test_txn.sign(issuer.private_key))

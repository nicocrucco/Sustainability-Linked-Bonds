"""
Sustainability Linked Bond - Algorand dApp
"""

__author__ = "Nicolò Crucco"

from algosdk.util import algos_to_microalgos

from pyteal import *

from beaker import *
from beaker.client import *
from beaker.decorators import *


class SLB(Application):
    #################
    #  GLOBAL STATE #
    #################
    oracle_address: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.bytes,
        default=Global.creator_address(),
        descr="KPI Oracle Address",
    )

    #################
    #  LOCAL STATE  #
    #################
    latest_kpi_update_timestamp: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Latest KPIs update timestamp",
    )

    kpi_a: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="KPI A: ...",
    )

    #################
    #   CONSTANTS   #
    #################
    kpi_time_delta: Final[Expr] = Int(3600)

    @create
    def create(self) -> Expr:
        return Seq(
            # Preconditions
            Assert(
                Txn.global_num_uints() == Int(self.app_state.schema().num_uints),
                Txn.global_num_byte_slices()
                == Int(self.app_state.schema().num_byte_slices),
                Txn.local_num_uints() == Int(self.acct_state.schema().num_uints),
                Txn.local_num_byte_slices()
                == Int(self.acct_state.schema().num_byte_slices),
            ),
            # Effects
            self.initialize_application_state(),
        )

    @opt_in
    def opt_in(self) -> Expr:
        return self.initialize_account_state()

    @external(authorize=Authorize.only(oracle_address))
    def update_investor_kpi(
        self,
        investor: abi.Account,
        new_kpi_a: abi.Uint64,
    ) -> Expr:
        """
        The Trusted Oracle can call this method to update Inverstors’ KPIs.
        Args:
            investor: Investor to update
            new_kpi_a: KPI A...
        """
        return Seq(
            # Preconditions
            Assert(
                Global.latest_timestamp()
                > self.latest_kpi_update_timestamp[investor.address()]
                + self.kpi_time_delta
            ),
            # Effects
            self.kpi_a[investor.address()].set(new_kpi_a.get()),
            self.latest_kpi_update_timestamp[investor.address()].set(
                Global.latest_timestamp()
            ),
        )


def demo() -> None:
    print("\n --- DEMO STARTS...")

    algod_client = sandbox.get_algod_client()

    slb_arranger = sandbox.get_accounts().pop()
    print("SLB Arranger Address:", slb_arranger.address)

    investor = sandbox.get_accounts().pop()
    print("Investor Address:", investor.address)

    # Create an Application client containing both an algod client and app
    slb_app_client = ApplicationClient(
        client=algod_client,
        app=SLB(),
        signer=slb_arranger.signer,
    )

    print("\n --- SLB Arranger creates and funds SLB application...")
    app_id, app_addr, txid = slb_app_client.create()
    slb_app_client.fund(algos_to_microalgos(10))
    print(f" --- App ID: {app_id}, dApp Address: {app_addr} created in tx: " f"{txid}")

    print("\n --- Investor opt-in SLB application...")
    slb_app_client.opt_in(signer=investor.signer)
    print(slb_app_client.get_account_state(investor.address))

    print("\n --- SLB Arranger updates Investor's KIPs...")
    slb_app_client.call(
        SLB.update_investor_kpi,
        investor=investor.address,
        new_kpi_a=10,
    )
    print(slb_app_client.get_account_state(investor.address))

    print("\n --- END OF DEMO!")


if __name__ == "__main__":
    demo()

"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import Contract
from moneyonchain.admin import ProxyAdmin


class MoCDecentralizedExchange(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MoCDecentralizedExchange.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MoCDecentralizedExchange.bin'))

    mode = 'DEX'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['dex']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.connection_manager)
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def token_pairs(self, block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        result = self.sc.functions.getTokenPairs().call(
            block_identifier=block_identifier)

        return result

    def token_pairs_status(self, base_address, secondary_address,
                           block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        base_address = Web3.toChecksumAddress(base_address)
        secondary_address = Web3.toChecksumAddress(secondary_address)

        result = self.sc.functions.getTokenPairStatus(base_address,
                                                      secondary_address).call(
            block_identifier=block_identifier)

        if result:
            d_status = dict()
            d_status['emergentPrice'] = result[0]
            d_status['lastBuyMatchId'] = result[1]
            d_status['lastBuyMatchAmount'] = result[2]
            d_status['lastSellMatchId'] = result[3]
            d_status['tickNumber'] = result[4]
            d_status['nextTickBlock'] = result[5]
            d_status['lastTickBlock'] = result[6]
            d_status['lastClosingPrice'] = result[7]
            d_status['disabled'] = result[8]
            d_status['EMAPrice'] = result[9]
            d_status['smoothingFactor'] = result[10]
            d_status['marketPrice'] = result[11]

            return d_status

        return result

    def convert_token_to_common_base(self,
                                     token_address,
                                     amount,
                                     base_address,
                                     formatted: bool = True,
                                     block_identifier: BlockIdentifier = 'latest'):
        """
        @dev simple converter from the given token to a common base, in this case, Dollar on Chain
        @param token_address the token address of token to convert into the common base token
        @param amount the amount to convert
        @param base_address the address of the base of the pair in witch the token its going to operate.
        if the the token it is allready the base of the pair, this parameter it is unimportant
        @return convertedAmount the amount converted into the common base token
        """

        token_address = Web3.toChecksumAddress(token_address)
        base_address = Web3.toChecksumAddress(base_address)

        result = self.sc.functions.convertTokenToCommonBase(token_address,
                                                            amount,
                                                            base_address).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def get_price_provider(self, base_address, secondary_address,
                           block_identifier: BlockIdentifier = 'latest'):
        """Returns the price provider of a given pair """

        base_address = Web3.toChecksumAddress(base_address)
        secondary_address = Web3.toChecksumAddress(secondary_address)

        result = self.sc.functions.getPriceProvider(base_address,
                                                    secondary_address).call(
            block_identifier=block_identifier)

        return result

    def next_tick(self, pair, block_identifier: BlockIdentifier = 'latest'):
        """ Next tick """

        result = self.sc.functions.getNextTick(pair[0], pair[1]).call(
            block_identifier=block_identifier)

        return result

    def are_orders_to_expire(self,
                             pair,
                             is_buy_order,
                             block_identifier: BlockIdentifier = 'latest'):
        """ Are orders to expire """

        result = self.sc.functions.areOrdersToExpire(pair[0],
                                                     pair[1],
                                                     is_buy_order).call(
            block_identifier=block_identifier)

        return result

    def emergent_price(self,
                       pair,
                       block_identifier: BlockIdentifier = 'latest'):
        """ Calculates closing price as if the tick closes at this moment.
            emergentPrice: AVG price of the last matched Orders

            return (emergentPrice, lastBuyMatch.id, lastBuyMatch.exchangeableAmount, lastSellMatch.id);
            """

        result = self.sc.functions.getEmergentPrice(pair[0], pair[1]).call(
            block_identifier=block_identifier)

        return result

    def market_price(self,
                     pair,
                     formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """ Get the current market price """

        result = self.sc.functions.getMarketPrice(pair[0], pair[1]).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def run_tick_for_pair(self, pair,
                          gas_limit=3500000,
                          wait_timeout=240,
                          matching_steps=70,
                          default_account=None,
                          wait_receipt=True):
        """Run tick for pair """

        tx_hash = None
        tx_receipt = None

        block_number = self.connection_manager.block_number
        self.log.info('About to run tick for pair {0}'.format(pair))
        next_tick_info = self.next_tick(pair)
        block_of_next_tick = next_tick_info[1]

        self.log.info('BlockOfNextTick {0}, currentBlockNumber {1}'.format(
            block_of_next_tick, block_number))
        self.log.info('Is tick runnable? {0}'.format(
            block_of_next_tick <= block_number))
        if block_of_next_tick <= block_number:

            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              'matchOrders',
                                                              pair[0],
                                                              pair[1],
                                                              matching_steps,
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            self.log.info(
                'Transaction hash of tick run {0}'.format(tx_hash.hex()))

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash,
                                                                                  timeout=wait_timeout,
                                                                                  poll_latency=0.5)

                self.log.info(
                    "Tick runned correctly in Block  [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                        tx_receipt['blockNumber'],
                        Web3.toHex(tx_receipt['transactionHash']),
                        tx_receipt['gasUsed'],
                        tx_receipt['from']))

        else:
            self.log.info('Block of next tick has not been reached\n\n')

        return tx_hash, tx_receipt

    def run_orders_expiration_for_pair(self, pair, is_buy_order, order_type,
                                       hint=0,
                                       order_id=0,
                                       gas_limit=3500000,
                                       wait_timeout=240,
                                       matching_steps=70,
                                       default_account=None,
                                       wait_receipt=True):
        """Run order expiration """

        tx_hash = None
        tx_receipt = None

        block_number = self.connection_manager.block_number

        self.log.info('About to expire {0} orders for pair {1} in blockNumber {2}'.format('buy' if is_buy_order else 'sell',
                                                                                          pair, block_number))

        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'processExpired',
                                                          pair[0],
                                                          pair[1],
                                                          is_buy_order,
                                                          hint,
                                                          order_id,
                                                          matching_steps,
                                                          order_type,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        self.log.info(
            'Transaction hash of {0} orders expiration {1}'.format('buy' if is_buy_order else 'sell',
                                                                   tx_hash.hex()))

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout,
                                                                              poll_latency=0.5)

            self.log.info(
                "Orders expiration job finished in block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                    tx_receipt['blockNumber'],
                    Web3.toHex(tx_receipt['transactionHash']),
                    tx_receipt['gasUsed'],
                    tx_receipt['from']))

        return tx_hash, tx_receipt


class BaseConstructor(Contract):
    log = logging.getLogger()

    contract_abi = None
    contract_bin = None

    mode = 'DEX'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def fnx_constructor(self, *tx_parameters, wait_receipt=True):
        """ Constructor deploy """

        sc, content_abi, content_bin = self.connection_manager.load_bytecode_contract(self.contract_abi,
                                                                                      self.contract_bin)
        tx_hash = self.connection_manager.fnx_constructor(sc, *tx_parameters)

        tx_receipt = None
        if wait_receipt:
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash)

        return tx_hash, tx_receipt


class TokenPriceProviderLastClosingPrice(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/TokenPriceProviderLastClosingPrice.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/TokenPriceProviderLastClosingPrice.bin'))

    mode = 'DEX'

    def constructor(self, base_token, secondary_token):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token)
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt


class MocBproBtcPriceProviderFallback(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocBproBtcPriceProviderFallback.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocBproBtcPriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(moc_state),
                                                   Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token)
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt


class MocBproUsdPriceProviderFallback(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocBproUsdPriceProviderFallback.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocBproUsdPriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(moc_state),
                                                   Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token)
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt


class UnityPriceProvider(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/UnityPriceProvider.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/UnityPriceProvider.bin'))

    mode = 'DEX'

    def constructor(self):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor()

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt


class ExternalOraclePriceProviderFallback(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/ExternalOraclePriceProviderFallback.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/ExternalOraclePriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, external_price_provider, base_token, secondary_token):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(external_price_provider),
                                                   Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token)
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt


class MocRiskProReservePriceProviderFallback(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocRiskProReservePriceProviderFallback.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocRiskProReservePriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(moc_state),
                                                   Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token)
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt


class MocRiskProUsdPriceProviderFallback(BaseConstructor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocRiskProUsdPriceProviderFallback.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MocRiskProUsdPriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['dex']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(moc_state),
                                                   Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token)
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Contract Address: {address}".format(address=tx_receipt.contractAddress))

        return tx_hash, tx_receipt

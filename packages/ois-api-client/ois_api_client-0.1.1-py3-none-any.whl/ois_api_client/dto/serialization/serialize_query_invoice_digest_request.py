import xml.etree.ElementTree as ET

from .serialize_additional_query_params import serialize_additional_query_params
from .serialize_basic_online_invoice_request import serialize_basic_online_invoice_request
from .serialize_element import serialize_text_element, serialize_int_element
from .serialize_mandatory_query_params import serialize_mandatory_query_params
from .serialize_relational_query_params import serialize_relational_query_params
from .serialize_transaction_query_params import serialize_transaction_query_params
from ..QueryInvoiceDigestRequest import QueryInvoiceDigestRequest


def serialize_query_invoice_digest_request(data: QueryInvoiceDigestRequest, request_signature: str,
                                           password_hash: str) -> ET.Element:
    root = serialize_basic_online_invoice_request(data, 'QueryInvoiceDigestRequest', request_signature, password_hash)

    serialize_int_element(root, 'page', data.page)
    serialize_text_element(root, 'invoiceDirection', data.invoice_direction.value)

    query_params_element = ET.SubElement(root, 'invoiceQueryParams')
    serialize_mandatory_query_params(query_params_element, data.invoice_query_params.mandatory_query_params.parameter)
    serialize_additional_query_params(query_params_element, data.invoice_query_params.additional_query_params)
    serialize_relational_query_params(query_params_element, data.invoice_query_params.relational_query_params)
    serialize_transaction_query_params(query_params_element, data.invoice_query_params.transaction_query_params)
    return root

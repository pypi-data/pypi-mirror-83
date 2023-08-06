"""
Copyright (C) Kehtra Pty Ltd - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""
import os
from datetime import datetime, timedelta
from typing import Union

from .decorators import refresh_token
from zeep import Client as zeep_client
from zeep.transports import Transport
from zeep.cache import InMemoryCache


class Ram:

    def __init__(self, user_id=None, password=None):
        transport = Transport(cache=InMemoryCache(timeout=(3600 * 24)))
        self.uploads_client = zeep_client('http://41.21.176.123/RAMConnectV2/Uploads/CustomerPortalWS.asmx?WSDL',
                                          transport=transport)
        self.tsm_client = zeep_client('http://41.21.176.123/ramconnectv2/Tracking/ServiceMessagesWS.asmx?WSDL',
                                      transport=transport)
        self.user_id = user_id or os.environ.get('RAM_USER_ID')
        self.password = password or os.environ.get('RAM_PASSWORD')
        token = self.uploads_client.service.Logon(user_id, password)
        if token is None:
            raise
        self.token = token
        self.expiry = datetime.now() + timedelta(minutes=20)
        self.expiry_delta = 60 * 2

    @refresh_token
    def logon(self, *args, **_) -> None:
        """
        Returns token to be used in further requests
        """
        if args is not None or len(args) == 0:
            res = self.uploads_client.service.Logon(*args)
            if res is not None:
                self.token = res
                self.token = self.uploads_client.service.Logon(self.user_id, self.password)
                self.expiry = datetime.now() + timedelta(minutes=20)
            else:
                raise
        else:
            self.token = self.uploads_client.service.Logon(self.user_id, self.password)
            self.expiry = datetime.now() + timedelta(minutes=20)

    @refresh_token
    def user_session_valid(self, *args, **_) -> bool:
        return self.uploads_client.service.UserSessionValid(self.user_id, self.token, *args)

    @refresh_token
    def consignment_id_from_shipper_reference(self, *args, **_) -> str:
        return self.uploads_client.service.ConsignmentID_FromShipperReference(self.user_id, self.token, *args)

    @refresh_token
    def label_xml(self, *args, **_) -> object:
        return self.uploads_client.service.Label_XML(self.user_id, self.token, *args)

    @refresh_token
    def upload_collection_request(self, *args, **_) -> str:
        return self.uploads_client.service.Upload_CollectionRequest(self.user_id, self.token, *args)

    @refresh_token
    def suburb_search(self, *args, **_) -> object:
        return self.uploads_client.service.SuburbSearch(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_get_by_status(self, *args, **_) -> object:
        return self.uploads_client.service.Upload_Consignment_GetByStatus(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_get_status(self, *args, **_) -> object:
        return self.uploads_client.service.Upload_Consignment_GetStatus(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment(self, *args, **_) -> int:
        return self.uploads_client.service.Upload_Consignment(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_minimal(self, *args, **_) -> int:
        return self.uploads_client.service.Upload_Consignment_Minimal(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_specify_sender(self, *args, **_) -> int:
        return self.uploads_client.service.Upload_Consignment_SpecifySender(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_including_parcels(self, *args, **_) -> int:
        return self.uploads_client.service.Upload_ConsignmentInclParcels(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_including_parcels_minimal(self, *args, **_) -> int:
        return self.uploads_client.service.Upload_ConsignmentInclParcels_Minimal(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_including_parcels_specify_sender(self, *args, **_) -> int:
        return self.uploads_client.service.Upload_ConsignmentInclParcels_SpecifySender(self.user_id, self.token, *args)

    @refresh_token
    def upload_parcel(self, *args, **_) -> bool:
        return self.uploads_client.service.Upload_Parcel(self.user_id, self.token, *args)

    @refresh_token
    def waybill(self, *args, **_) -> Union[str, None]:
        return self.uploads_client.service.Waybill(self.user_id, self.token, *args)

    @refresh_token
    def waybill_from_shipper_reference(self, *args, **_) -> Union[str, None]:
        return self.uploads_client.service.Waybill_FromShipperReference(self.user_id, self.token, *args)

    """
    --------------------------
    Fields returned per record
    --------------------------
    
    DateTime            datetime            Time of the track event
    TrackType           string              Type of track – see list
    Hub                 string              Which hub it was tracked in
    Description         string              Human readable tracking details
    Driver              string              Responsible driver
    ConsignmentStatus   string              Current status of consignment
    """

    def consignment_tracking(self, *args, **_):
        """
        track using the unique ConsignmentID of the consignment.
        :return:
        """
        return self.uploads_client.service.ConsignmentTracking(self.user_id, self.token, *args)

    def consignment_tracking_by_shipper_reference(self, *args, **_):
        """
         track using the client’s own reference.
        :return:
        """
        return self.uploads_client.service.ConsignmentTrackingByShipperReference(self.user_id, self.token, *args)

    @refresh_token
    def generic_messages_get_batch(self, *args, **_) -> object:
        return self.tsm_client.service.GenericMessages_GetBatch(self.user_id, self.token)

    @refresh_token
    def generic_messages_get_batch_typed(self, *args, **_) -> object:
        """
        Get the next batch of tracking and status messages. The return value will be strongly typed.
        This call has to be followed by a call to GenericMessages_UpdateBatch to confirm batch download success.
        Please note that Message elements might in future contain extra attributes.
        :return:
        """
        return self.tsm_client.service.GenericMessages_GetBatch_Typed(self.user_id, self.token)

    @refresh_token
    def generic_messages_update_batch(self, *args, **_) -> bool:
        """
        Confirm the download status of the batch
        :param args: BatchID, SendResult, Success, Failed
        :return:
        """
        return self.tsm_client.service.GenericMessages_UpdateBatch(self.user_id, self.token, *args)

    @refresh_token
    def pod_images_as_pdf(self, *args, **_) -> any:
        """
        Retrieve all the POD images for a consignment as a single PDF.
        :param args:
        :return:
        """
        return self.tsm_client.service.PODImagesAsPDF(self.user_id, self.token, *args)

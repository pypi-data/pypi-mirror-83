#
# Autogenerated by Thrift Compiler (0.11.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []


class Iface(object):
    def authenticateApplication(self, tAuthInfo):
        """
        Parameters:
         - tAuthInfo
        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def authenticateApplication(self, tAuthInfo):
        """
        Parameters:
         - tAuthInfo
        """
        self.send_authenticateApplication(tAuthInfo)
        return self.recv_authenticateApplication()

    def send_authenticateApplication(self, tAuthInfo):
        self._oprot.writeMessageBegin('authenticateApplication', TMessageType.CALL, self._seqid)
        args = authenticateApplication_args()
        args.tAuthInfo = tAuthInfo
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_authenticateApplication(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = authenticateApplication_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.ke is not None:
            raise result.ke
        if result.ae is not None:
            raise result.ae
        if result.ce is not None:
            raise result.ce
        raise TApplicationException(TApplicationException.MISSING_RESULT, "authenticateApplication failed: unknown result")


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["authenticateApplication"] = Processor.process_authenticateApplication

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_authenticateApplication(self, seqid, iprot, oprot):
        args = authenticateApplication_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = authenticateApplication_result()
        try:
            result.success = self._handler.authenticateApplication(args.tAuthInfo)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except koverse.thriftgen.ttypes.TKoverseException as ke:
            msg_type = TMessageType.REPLY
            result.ke = ke
        except koverse.thriftgen.security.ttypes.TAuthorizationException as ae:
            msg_type = TMessageType.REPLY
            result.ae = ae
        except koverse.thriftgen.security.ttypes.TCannotUseKoverseException as ce:
            msg_type = TMessageType.REPLY
            result.ce = ce
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("authenticateApplication", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class authenticateApplication_args(object):
    """
    Attributes:
     - tAuthInfo
    """


    def __init__(self, tAuthInfo=None,):
        self.tAuthInfo = tAuthInfo

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.tAuthInfo = koverse.thriftgen.security.ttypes.TAuthInfo()
                    self.tAuthInfo.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('authenticateApplication_args')
        if self.tAuthInfo is not None:
            oprot.writeFieldBegin('tAuthInfo', TType.STRUCT, 1)
            self.tAuthInfo.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(authenticateApplication_args)
authenticateApplication_args.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'tAuthInfo', [koverse.thriftgen.security.ttypes.TAuthInfo, None], None, ),  # 1
)


class authenticateApplication_result(object):
    """
    Attributes:
     - success
     - ke
     - ae
     - ce
    """


    def __init__(self, success=None, ke=None, ae=None, ce=None,):
        self.success = success
        self.ke = ke
        self.ae = ae
        self.ce = ce

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = koverse.thriftgen.security.ttypes.TAuthInfo()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.ke = koverse.thriftgen.ttypes.TKoverseException()
                    self.ke.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.ae = koverse.thriftgen.security.ttypes.TAuthorizationException()
                    self.ae.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRUCT:
                    self.ce = koverse.thriftgen.security.ttypes.TCannotUseKoverseException()
                    self.ce.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('authenticateApplication_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.ke is not None:
            oprot.writeFieldBegin('ke', TType.STRUCT, 1)
            self.ke.write(oprot)
            oprot.writeFieldEnd()
        if self.ae is not None:
            oprot.writeFieldBegin('ae', TType.STRUCT, 2)
            self.ae.write(oprot)
            oprot.writeFieldEnd()
        if self.ce is not None:
            oprot.writeFieldBegin('ce', TType.STRUCT, 3)
            self.ce.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(authenticateApplication_result)
authenticateApplication_result.thrift_spec = (
    (0, TType.STRUCT, 'success', [koverse.thriftgen.security.ttypes.TAuthInfo, None], None, ),  # 0
    (1, TType.STRUCT, 'ke', [koverse.thriftgen.ttypes.TKoverseException, None], None, ),  # 1
    (2, TType.STRUCT, 'ae', [koverse.thriftgen.security.ttypes.TAuthorizationException, None], None, ),  # 2
    (3, TType.STRUCT, 'ce', [koverse.thriftgen.security.ttypes.TCannotUseKoverseException, None], None, ),  # 3
)
fix_spec(all_structs)
del all_structs


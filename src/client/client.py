"""Iris Flow GUI - gRPC client wrapper.

Encapsulates all gRPC communication with the Iris Flow server.
Provides a clean interface for the UI layer to call without
dealing with protobuf or gRPC details directly.
"""

import grpc
from src.client import iris_flow_pb2, iris_flow_pb2_grpc


class IrisFlowClient:
    """Thread-safe gRPC client for Iris Flow server communication."""

    def __init__(self, address: str = "localhost:50052", timeout: float = 2.0):
        self._address = address
        self._timeout = timeout
        self._channel: grpc.Channel = None
        self._stub: iris_flow_pb2_grpc.IrisFlowStub = None
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self) -> bool:
        """Establish connection and verify with health check."""
        try:
            self._channel = grpc.insecure_channel(self._address)
            self._stub = iris_flow_pb2_grpc.IrisFlowStub(self._channel)
            resp = self._stub.HealthCheck(
                iris_flow_pb2.HealthRequest(), timeout=self._timeout
            )
            self._connected = (resp.status == "SERVING")
        except Exception:
            self._connected = False
            self._channel = None
            self._stub = None
        return self._connected

    def disconnect(self):
        """Close the gRPC channel."""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stub = None
            self._connected = False

    def get_status(self) -> dict:
        """Get current camera/stream status."""
        if not self._stub:
            return {"state": 0, "fps": 0, "sensor": "unknown"}
        try:
            resp = self._stub.GetStatus(
                iris_flow_pb2.StatusRequest(), timeout=self._timeout
            )
            return {
                "state": resp.state,
                "fps": resp.fps,
                "sensor": resp.sensor,
            }
        except Exception:
            self._connected = False
            return {"state": 0, "fps": 0, "sensor": "unknown"}

    def start_stream(self, width: int = 1920, height: int = 1080,
                     fmt: int = 1, fps: int = 30) -> dict:
        """Start a camera stream with the given configuration."""
        if not self._stub:
            return {"success": False, "error": "Not connected"}
        try:
            cfg = iris_flow_pb2.StreamConfig(
                width=width, height=height, format=fmt, fps=fps
            )
            resp = self._stub.StartStream(cfg, timeout=5.0)
            return {"success": resp.success, "error": resp.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stop_stream(self) -> dict:
        """Stop the currently running camera stream."""
        if not self._stub:
            return {"success": False, "error": "Not connected"}
        try:
            resp = self._stub.StopStream(
                iris_flow_pb2.StreamRequest(), timeout=5.0
            )
            return {"success": resp.success, "error": resp.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_isp(self, brightness: int = 128, contrast: int = 128,
                saturation: int = 128, sharpness: int = 128) -> dict:
        """Apply ISP tuning parameters."""
        if not self._stub:
            return {"success": False, "error": "Not connected"}
        try:
            cfg = iris_flow_pb2.IspConfig(
                brightness=brightness, contrast=contrast,
                saturation=saturation, sharpness=sharpness
            )
            resp = self._stub.SetIsp(cfg, timeout=5.0)
            return {"success": resp.success, "error": ""}
        except Exception as e:
            return {"success": False, "error": str(e)}

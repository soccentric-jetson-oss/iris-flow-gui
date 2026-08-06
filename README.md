# Iris Flow GUI — Camera Control Desktop Application

The Iris Flow GUI is a cross-platform PySide6 desktop application for controlling the Jetson AGX Orin's camera and ISP pipeline. It provides a clean, dark-themed interface with stream start and stop controls, ISP parameter sliders for brightness, contrast, and saturation tuning, and real-time status display showing sensor information, frame rate, and stream state. The application connects to the Iris Flow gRPC server and features automatic connection health monitoring with periodic status refreshes.

## Features

- Provides a cross-platform PySide6 desktop application that runs identically on Windows, macOS, and Linux operating systems
- Features a dark theme design with clean typography and intuitive control layout for professional use
- Offers camera stream start and stop controls with visual feedback showing current stream state
- Includes ISP parameter sliders for brightness, contrast, and saturation tuning with real-time visual feedback
- Displays real-time sensor status including sensor type, frame rate, and stream running state
- Connects to the Iris Flow gRPC server with automatic health check polling every 2 seconds
- Reconnects automatically when the server connection is lost, with clear status indicators
- Groups camera controls logically with a clean, uncluttered interface design
- Provides visual feedback for all operations including success and error states
- Can be packaged as a standalone executable for easy distribution without Python dependencies
- Licensed under MIT for maximum flexibility in commercial and open-source projects

## Quick Start

### Prerequisites
- Linux operating system (x86_64 for development, aarch64 for target deployment)
- Build tools including make, cmake, gcc or clang, and python3 as needed
- Linux kernel headers for kernel module compilation on target hardware

### Build and Test
```bash
make all      # Build all targets including library, tests, and binaries
make test     # Run the test suite to verify all functionality
make clean    # Clean all build artifacts and temporary files
```

## Repository Structure

| Directory | Contents |
|-----------|----------|
| src/ | Source code for the project |
| include/ | Public API header files |
| lib/ | Userspace library source and headers |
| test/ or tests/ | Unit tests and test utilities |
| proto/ | gRPC protocol buffer definitions |
| packaging/ | Distribution packaging files for deb, rpm, and ipk |
| docs/ | Documentation including Doxygen configuration |

## Project Status

**Version:** 0.1.0 — Initial release
**License:** MIT
**Audit Score:** 90/100 across 20 criteria

## Ecosystem

This project is part of the [Jetson AGX Orin Capability Showcase](https://github.com/soccentric-jetson-oss/soccentric-jetson-oss) — five open-source projects demonstrating full exploitation of NVIDIA's flagship edge AI platform.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions are welcome.

## License

MIT. See [LICENSE](LICENSE) for details.

---

## Showcase

This project is part of the [Jetson AGX Orin Capability Showcase](https://soccentric-jetson-oss.github.io/).

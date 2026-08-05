# Iris Flow GUI — Camera Control Desktop Application

The Iris Flow GUI is a cross-platform PySide6 desktop application for controlling the Jetson AGX Orin's camera and ISP pipeline. It provides a clean, dark-themed interface with stream start/stop controls, ISP parameter sliders for brightness, contrast, and saturation tuning, and real-time status display showing sensor information, frame rate, and stream state. The application connects to the Iris Flow gRPC server and features automatic connection health monitoring with periodic status refreshes. The intuitive layout groups camera controls logically, with visual feedback for all operations. The application is packaged as a standalone executable and supports Windows, macOS, and Linux deployment.

## Features

- Cross-platform
- PySide6
- desktop
- application
- Dark
- theme
- design
- Camera
- stream
- start/stop
- controls
- ISP
- parameter
- sliders
- (brightness,
- contrast,
- saturation)
- Real-time
- sensor
- status
- display
- Frame
- rate
- and
- stream
- state
- monitoring
- gRPC
- client
- with
- auto-reconnect
- Periodic
- health
- check
- polling
- Intuitive
- control
- layout
- Visual
- feedback
- for
- all
- operations
- Standalone
- executable
- packaging
- MIT
- licensed

## Quick Start

### Prerequisites
- Linux (x86_64 for development, aarch64 for target)
- Build tools (make, cmake, gcc/clang, python3)

### Build & Test
```bash
make all      # Build all targets
make test     # Run tests
make clean    # Clean build artifacts
```

## Repository Structure

| Directory | Contents |
|-----------|----------|
| `src/` | Source code |
| `include/` | Public API headers |
| `lib/` | Userspace library |
| `test/` | Unit tests |
| `proto/` | gRPC protocol definitions |
| `packaging/` | Distribution packages |
| `docs/` | Documentation |

## Project Status

**Version:** 0.1.0 — Initial release
**License:** MIT
**Audit Score:** 90/100

## Ecosystem

This project is part of the [Jetson AGX Orin Capability Showcase](https://github.com/soccentric-jetson-oss/soccentric-jetson-oss) — five open-source projects demonstrating full exploitation of NVIDIA's flagship edge AI platform.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions welcome!

## License

MIT. See [LICENSE](LICENSE) for details.

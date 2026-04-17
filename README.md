# Data Import Evidence Helper (CSS Override Tool)

This browser extension, named "Data Import Evidence Helper," is designed to assist Quality Assurance (QA) professionals and test engineers in capturing evidence during testing. It achieves this by dynamically expanding grids and applying local CSS overrides to prevent content overflow on web pages, ensuring that all necessary information is visible and can be accurately captured for documentation.

**Note:** This tool is developed for use within specific internal, non-public testing environments. Its purpose on GitHub is to showcase the technical approach and problem-solving skills in developing specialized QA tools, rather than to provide a publicly runnable utility.

## Features

- **Grid Expansion:** Automatically expands data grids on web pages to reveal all content.
- **CSS Overrides:** Applies custom CSS to prevent text and element overflow, ensuring full visibility.
- **Evidence Capture:** Facilitates comprehensive screenshot and video capture by optimizing page layout.
- **Simple Activation:** Easily activated via a browser action button.

## How it Works

The extension operates by injecting JavaScript and CSS into the active tab when its action button is clicked. It targets common grid structures and applies styles that force expansion and prevent overflow, making it easier to capture complete views of complex data tables or UI elements.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mihaimx1/css-override-tool.git
   ```
2. **Open your Chromium-based browser** (e.g., Google Chrome, Microsoft Edge).
3. Navigate to `chrome://extensions`.
4. Enable **Developer mode** using the toggle switch in the top right corner.
5. Click on **Load unpacked** and select the cloned `css-override-tool` directory.

The extension will now be installed and visible in your browser's extension toolbar.

## Usage

1. Navigate to the web page where you need to capture evidence, especially pages with data grids or elements that tend to overflow.
2. Click on the "Data Import Evidence Helper" extension icon in your browser's toolbar.
3. The extension will automatically apply its CSS overrides and expand relevant elements, preparing the page for evidence capture.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the functionality or address any bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

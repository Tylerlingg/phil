// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract chaosPhil is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    IERC20 private memecoin;

    uint256 public constant MAX_SUPPLY = 7777;
    uint256 public constant ETC_PRICE = 1 ether;
    uint256 public constant MEMECOIN_PRICE = 69 * 10**18;

    // Define trait categories
    enum TraitCategory { Bg, Phil, Spikes, Neck, Top, Teeth, TopJaw, Eyes }

    // Mapping to store base layer SVG data per category in Base64 format
    mapping(TraitCategory => string) private baseLayerSvgData;

    // Event to log when base layer data is stored
    event BaseLayerStored(TraitCategory indexed category, string data);

    // Event to log when NFT is   minted
    event NFTMinted(address indexed owner, uint256 indexed tokenId, string tokenURI);

    // Constructor to set token name, symbol, and memecoin address
    constructor(address memecoinAddress) ERC721("Phil", "PHIL") Ownable(msg.sender) {
        memecoin = IERC20(memecoinAddress);
    }

    /**
     * @dev Stores Base64 SVG data for a specific base layer category.
     * Can only be called by the contract owner.
     * @param category The category of the base layer.
     * @param data The Base64 SVG data to store.
     */
    function storeBaseLayer(TraitCategory category, string memory data) public onlyOwner {
        require(bytes(data).length > 0, "Data should not be empty");
        baseLayerSvgData[category] = data;
        emit BaseLayerStored(category, data);
    }

    /**
     * @dev Retrieves Base64 SVG data for a specific base layer category.
     * @param category The category of the base layer.
     * @return The Base64 SVG data for the specified category.
     */
    function getBaseLayer(TraitCategory category) public view returns (string memory) {
        return baseLayerSvgData[category];
    }

    /**
     * @dev Compiles an SVG from provided trait data and base layers.
     * @param traitData An array of trait data in Base64 format.
     * @return The compiled SVG as a Base64 string.
     */
    function compileSvg(string[9] memory traitData) public view returns (string memory) {
        string memory svgHeader = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'>";
        string memory svgFooter = "</svg>";
        string memory svgContent = "";

        for (uint256 i = 0; i < traitData.length; i++) {
            svgContent = string(abi.encodePacked(svgContent, "<image xlink:href='data:image/svg+xml;base64,", baseLayerSvgData[TraitCategory(i)], "'/>", traitData[i]));
        }

        return string(abi.encodePacked(svgHeader, svgContent, svgFooter));
    }

    /**
     * @dev Mints a new NFT with specified traits.
     * @param traitData An array of Base64 trait data to include in the SVG.
     */
    function mintNFT(string[9] memory traitData) public payable {
        require(_tokenIds.current() < MAX_SUPPLY, "Maximum supply reached");
        require(traitData.length == 9, "Trait data must have 9 elements");

        uint256 newItemId = _tokenIds.current();
        _tokenIds.increment();

        if (msg.value == ETC_PRICE) {
            // Paid with ETC
        } else {
            // Paid with memecoin
            require(memecoin.transferFrom(msg.sender, address(this), MEMECOIN_PRICE), "Memecoin transfer failed");
        }

        string memory svg = compileSvg(traitData);
        string memory tokenURI = string(abi.encodePacked("data:image/svg+xml;base64,", base64(bytes(svg))));

        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);

        emit NFTMinted(msg.sender, newItemId, tokenURI);
    }

    /**
     * @dev Encodes bytes to a base64 string.
     * @param data The data to encode.
     * @return The base64 encoded string.
     */
    function base64(bytes memory data) internal pure returns (string memory) {
        bytes memory alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        uint256 encodedLen = 4 * ((data.length + 2) / 3);
        bytes memory result = new bytes(encodedLen + 1);

        for (uint256 i = 0; i < data.length; i += 3) {
            uint256 a = uint8(data[i]);
            uint256 b = i + 1 < data.length ? uint8(data[i + 1]) : 0;
            uint256 c = i + 2 < data.length ? uint8(data[i + 2]) : 0;

            result[i / 3 * 4] = alphabet[a >> 2];
            result[i / 3 * 4 + 1] = alphabet[((a & 3) << 4) | (b >> 4)];
            result[i / 3 * 4 + 2] = alphabet[((b & 15) << 2) | (c >> 6)];
            result[i / 3 * 4 + 3] = alphabet[c & 63];
        }

        if ((data.length % 3) == 1) {
            result[encodedLen - 1] = '=';
            result[encodedLen - 2] = '=';
        } else if ((data.length % 3) == 2) {
            result[encodedLen - 1] = '=';
        }

        result[encodedLen] = 0;
        return string(result);
    }
}

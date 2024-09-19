# phil
phil is a work in progress Generative Art Project on ethereum Classic based on the Philosoraptor meme. 

I'm open-sourcing it because i've got lost in the sauce of life as well as this project and since i've never really been a developer or coder i figured this would be a good try at my first legit repo.

In order to achieve the functionality thus far I've relied 100% on ChatGPT by OpenAI. Like I stated before, this is my first legit try at a repo, and I also didn't know what Computer Science was 3 years ago. 

Abstract: 

phil is a fully on-chain NFT project inspired by Avastars and people i've learned from and respect within the crypto space. It aims to achieve full decentralization and on-chain storage using ethscriptions on ethereum Classic. phil’s artwork is made up of 9 distinct trait SVG layers created by using different algorthims, which are then compressed, stored, and referenced on-chain.

	Examples of Algorithms used will be created in a different file titled 'GitchArt.js'. 

phil currently has 9 different layers:

    const traitBaseCategories = ['Color', 'Bg', 'PhilBody', 'Spikes', 'Neck', 'Top', 'Teeth', 'TopJaw', 'Eyes'];

The layers are listed from back to front. 

User Experience Overview:

	1.	Website Interaction:
	•	When a user visits the website, a random combination of traits will be generated based on their rarity and a scrolling mechanism will be set in place to where the user can keep scrolling through images until they land on one they fuck with.
	•	Traits are categorized into four rarities: Common, Uncommon, Rare, and Legendary.
	•	Rarities are defined by the following weights:

      // Rarity weights
      const rarityWeights = {
        common: 50,
        uncommon: 30,
        rare: 15,
        legendary: 5,
      };


    2. Minting the NFT:

	•	Users scroll through combinations until they find a Phil they fuck with.
	•	Upon clicking “mint”, the user only pays the gas fee.
	•	The NFT is minted to a newly created vanity address, and a memecoin called $phil will also be sent to this address ($phil will be deployed separately and is another topic of conversation).
	•	The goal is to allow the user to recover their private key offline, ensuring full anonymity (not sure how the fuck we do this honestly)

Developer Overview:

The goal is to ensure that all data for the NFTs is stored entirely on-chain, then using ethscriptions on ethereum Classic, while users are able to keep complete anonimity when claiming their own phil. 

	1.	Compression and Storage:

	SVG to Hexadecimal Conversion
	•	Start with SVGs.
	•	Compress using SVGO.
	•	Convert to base64 strings.
	•	Compress with Brotli.
	•	Convert the compressed string to hexadecimal.
	•	Each final hexadecimal string is stored as an ethscription.
     *each hash can be stored within the Smart Contract as a .json file converted into a hexadecmial which the front end could then reference so it's not pulling from a computer or centralized server. I'm not sure if it would be possible to store all the hashes from the .json file in one Smart Contract, but if not, it's always possible to seperate the cetegories and deploy multiple Smart Contracts for the frontend to reference. 

	2.	Data Flow:

	•	Each layer (trait) is stored on-chain via ethscriptions.
	•	The transaction hashes (ethscription pointers) are stored in a .json file which are then converted into hexadecimal format and stored in the Smart Contract.
	•	On the frontend, traits are decompressed and combined to create the final phil image.

	3.	Minting Process:

	•	When a user mints, the smart contract references 9 ethscription pointers (one for each trait).
	•	The smart contract ensures no two phils are generated with the same trait combination by tracking used combinations and preventing duplicates.

	4.	Token Delivery:

	•	The NFT is minted to the newly generated vanity address.
	•	Simultaneously, $phil tokens are sent to the same address.

	5.	Minting Details:

	•	Minting will be open for 369 days, though the total quantity is still to be determined.
	•	Feedback on whether a maximum supply should be set is welcome.


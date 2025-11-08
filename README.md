# Tengwar & Black Speech Translator

A Python-based GUI application that converts English text into Tengwar script (Elvish writing) and Black Speech (the language of Mordor), inspired by J.R.R. Tolkien's Middle-Earth.

## Features

- **Tengwar Script Translation**: Convert English text to Tengwar script for use with the Tengwar Annatar font
- **Black Speech Translation**: Translate English words and phrases to Black Speech with phonetic adaptations
- **User-Friendly GUI**: Simple interface built with Tkinter
- **Copy to Clipboard**: Easily copy translated text for use in other documents
- **Dual Mode Support**: Switch between Tengwar and Black Speech conversion modes

## Screenshots

The application features two conversion modes:
- **Tengwar Mode**: Transliterates English to Tengwar script (requires Tengwar Annatar font for proper display)
- **Black Speech Mode**: Translates English to Black Speech with a comprehensive dictionary and phonetic rules

## Prerequisites

- Python 3.9 or higher
- Conda (recommended) or pip
- **Tengwar Annatar font** (required for Tengwar script display)

### Installing the Tengwar Annatar Font

1. Download the Tengwar Annatar font from one of these sources:
   - [Free Tengwar Font Project](http://freetengwar.sourceforge.net/)
   - Search for "Tengwar Annatar font download"

2. Install the font on your system:
   - **Windows**: Right-click the `.ttf` file and select "Install"
   - **macOS**: Double-click the `.ttf` file and click "Install Font"
   - **Linux**: Copy the `.ttf` file to `~/.fonts/` and run `fc-cache -f -v`

## Installation

### Option 1: Using Conda (Recommended)

1. Clone or download this repository:
```bash
git clone <your-repo-url>
cd "Tengwar and Black Speech"
```

2. Create the conda environment:
```bash
conda env create -f environment.yml
```

3. Activate the environment:
```bash
conda activate tengwar-translator
```

### Option 2: Using pip

1. Clone or download this repository:
```bash
git clone <your-repo-url>
cd "Tengwar and Black Speech"
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the GUI Application

Simply run the launcher script:

```bash
python launch_gui.py
```

Or run the main module directly:

```bash
python english_to_tengwar.py
```

### Using the Application

1. **Select Conversion Mode**: Choose between "Tengwar Script" or "Black Speech" using the radio buttons at the top

2. **Enter Text**: Type or paste your English text in the input box

3. **Convert**: Click the "Convert to Tengwar" or "Convert to Black Speech" button

4. **View Results**:
   - For **Tengwar**: The output will appear in Tengwar script (make sure you have the Tengwar Annatar font installed)
   - For **Black Speech**: The output will appear as transliterated text

5. **Copy Results**: Click "Copy Result" to copy the translated text to your clipboard

6. **Clear**: Click "Clear" to reset both input and output fields

### Using as a Python Module

You can also use the conversion functions in your own Python scripts:

```python
from english_to_tengwar import convert_tengwar, convert_black_speech

# Convert to Tengwar
tengwar_text = convert_tengwar("This was a triumph!")
print(tengwar_text)  # Display in Tengwar Annatar font

# Convert to Black Speech
black_speech_text = convert_black_speech("One Ring to rule them all")
print(black_speech_text)  # Output: ash nazg gimbatul agh burzum-ishi
```

## How It Works

### Tengwar Mode

The Tengwar transliteration follows personal preferences extracted from the Tengwar Textbook:
- Handles vowel carriers and tehtar (vowel marks)
- Distinguishes between voiced and voiceless 'th'
- Supports double consonants (ch, sh, zh, ph, kh, gh, ng, rd, ld)
- Uses the R-rule for pre-vowel 'r'
- Handles special cases like "of" and "the"

**Special Characters** (for manual input):
- `T` = theta (voiceless th)
- `D` = eth (voiced th)
- `R` = pre-vowel r
- `S`, `Z` = vowel-less s and z
- `Q` = rd, `L` = ld
- `W` = wh, `C` = ch, `K` = kh
- `G` = gh, `X` = sh, `H` = zh
- `N` = ng

### Black Speech Mode

The Black Speech translator includes:
- **Comprehensive dictionary**: 200+ word mappings including Ring inscription vocabulary
- **Phonetic transformation**: Unknown words are adapted to sound harsh and guttural
- **Authentic sound**: Follows Tolkien's harsh, dark linguistic patterns

Example translations:
- "One Ring to rule them all" → "ash nazg gimbatul agh burzum-ishi"
- "darkness" → "burzum"
- "power" → "gash"

## File Structure

```
Tengwar and Black Speech/
├── english_to_tengwar.py      # Main conversion module with GUI
├── launch_gui.py               # Simple launcher script
├── environment.yml             # Conda environment configuration
├── condaenv.*.requirements.txt # Auto-generated requirements file
└── README.md                   # This file
```

## Testing

The code includes unit tests based on a blog post example. To run tests:

```bash
python -m unittest english_to_tengwar
```

## Limitations and Future Improvements

- Tengwar numerals not yet implemented (shows placeholders)
- Some edge cases in phonetic conversion may need refinement
- Black Speech vocabulary is based on available Tolkien canon and educated linguistic extrapolation
- Currently optimized for the Tengwar Annatar font (future support for TengwarScript TeX package planned)

## Credits

- **Tengwar writing system**: Created by J.R.R. Tolkien
- **Tengwar Annatar font**: Created by Johan Winge
- **Transliteration rules**: Based on the Tengwar Textbook
- **Black Speech**: Linguistic framework by J.R.R. Tolkien

## License

This project is provided as-is for educational and recreational purposes. The Tengwar script and Black Speech are creative works of J.R.R. Tolkien and the Tolkien Estate.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

Special thanks to the Tolkien fan community and linguists who have documented and preserved these beautiful writing systems and languages.

---

**Note**: This translator uses a personal mode of Tengwar transliteration. Different modes exist, and this implementation reflects one particular approach to writing English in Tengwar script.

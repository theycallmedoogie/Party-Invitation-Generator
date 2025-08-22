# Party Invitation Generator

A Python application that creates beautiful, graphical party invitations with festive themes and customizable text.

## Features

### 🎨 Multiple Generation Methods
- **Artistic Generator** - Creates beautiful invitations using Pillow with gradients, balloons, and confetti
- **AI Generator** - Uses Stable Diffusion for photo-realistic backgrounds (requires GPU setup)
- **Simple Generator** - Lightweight version for basic needs

### 🎭 Theme Options
1. **Celebration** - Bright coral, orange, yellow, and cyan colors
2. **Elegant** - Purple and lavender tones
3. **Tropical** - Pink and coral beach vibes
4. **Sunset** - Orange and yellow warm colors

### ✨ Visual Elements
- Colorful gradient backgrounds
- Animated balloon decorations with highlights
- Scattered confetti effects
- Professional text overlays with semi-transparent backgrounds
- High-quality 800x600 output resolution

### 📝 Customizable Content
- Party title
- Date and time
- Location details
- RSVP information
- Theme selection

## Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
# Run the main artistic generator
python artistic_party_generator.py

# For AI-powered generation (requires GPU setup)
python party_invitation_generator.py
```

### Example Output
The generator creates invitations like:
- Background: Colorful gradient with festive decorations
- Text: Professional layout with party details
- Format: High-quality PNG files ready for printing or digital sharing

## File Structure
```
Party Invitation Generator/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── artistic_party_generator.py  # Main generator (recommended)
├── party_invitation_generator.py # AI-powered version
├── simple_party_generator.py    # Lightweight version
└── party_invitation_celebration.png # Sample output
```

## Usage Examples

### Interactive Mode
Run the main generator and follow the prompts:
```bash
python artistic_party_generator.py
```

### Programmatic Usage
```python
from artistic_party_generator import create_party_invitation, save_invitation

# Custom party details
party_info = {
    'title': 'Birthday Bash!',
    'date': 'Friday, December 25th',
    'time': '8:00 PM',
    'location': '456 Celebration Ave',
    'rsvp': 'RSVP: birthday@party.com'
}

# Generate invitation
invitation = create_party_invitation(party_info, theme="sunset")
save_invitation(invitation, "my_party.png")
```

## Themes Preview

- **Celebration**: Vibrant mix of coral, orange, yellow, and cyan
- **Elegant**: Sophisticated purple gradients
- **Tropical**: Warm pink and coral tones
- **Sunset**: Rich orange to yellow gradients

## Technical Details

### Dependencies
- **Pillow (PIL)**: Image generation and manipulation
- **Matplotlib**: Graphics and visual effects
- **NumPy**: Mathematical operations for gradients

### AI Version (Optional)
- **PyTorch**: Deep learning framework
- **Diffusers**: Stable Diffusion implementation
- **Transformers**: Model support
- **CUDA Support**: For GPU acceleration (optional)

### Output Specifications
- **Resolution**: 800x600 pixels
- **Format**: PNG with high quality
- **Color Space**: RGB
- **File Size**: Typically 200-500KB

## Troubleshooting

### Common Issues
1. **Font Loading**: Falls back to system fonts if custom fonts unavailable
2. **GPU Setup**: AI version works on CPU but slower without GPU
3. **Dependencies**: Install all requirements for full functionality

### Performance Tips
- Use `artistic_party_generator.py` for fastest results
- GPU acceleration improves AI generation speed significantly
- Large batch generation benefits from programmatic usage

## Contributing

This project is designed for personal and educational use. Feel free to:
- Modify themes and colors
- Add new decoration patterns
- Enhance text formatting
- Create additional output formats

## License

Created for personal use. Modify and distribute as needed.

## Version History

- **v1.0**: Initial release with artistic generation
- **v1.1**: Added AI-powered generation option
- **v1.2**: Multiple theme support and improved UI

---

**Created with**: Python 3.13, Pillow, Matplotlib
**Platform**: Windows (tested), should work cross-platform
**GPU**: Optional for AI features, RTX 4060 recommended
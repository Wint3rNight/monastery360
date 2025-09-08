# Monastery360 - Panoramic Image System

## Overview

This document describes how the 360° panoramic virtual tour system works for Sikkim monasteries.

## Current Implementation

### Panoramic Image Sources
The system now uses curated high-quality images from Unsplash that are relevant to Sikkim monasteries and Buddhist architecture. Each monastery has specific panoramic views configured with appropriate viewing angles and zoom levels.

### Configuration File
Location: `/static/data/monastery_panoramas.json`

This JSON file contains:
- **URL**: High-quality panoramic image URL
- **Title**: Descriptive title for the panoramic view
- **Description**: Detailed description of what the view shows
- **Credit**: Photo attribution
- **Viewing Parameters**: Initial yaw, pitch, and field of view settings
- **Type**: Image projection type (equirectangular)

### Monastery Panoramas

1. **Rumtek Monastery** - Main Hall view showcasing Tibetan Buddhist architecture
2. **Pemayangtse Monastery** - Courtyard view with Himalayan backdrop
3. **Enchey Monastery** - Prayer Hall interior with traditional murals
4. **Tashiding Monastery** - Sacred hilltop panoramic view
5. **Dubdi Monastery** - Ancient structure showcasing historical significance
6. **Phodong Monastery** - Mountain monastery complex view
7. **Labrang Monastery** - Sacred ceremonial hall interior
8. **Ralang Monastery** - Festival ground courtyard view
9. **Sangachoeling Monastery** - Historical ruins with mountain setting
10. **Ralong Monastery** - Panoramic mountain view

## Technical Implementation

### Files Updated
- `/templates/tours/monastery_detail.html` - Main detail view with enhanced panoramic viewer
- `/templates/tours/monastery_tour.html` - Individual monastery tour page
- `/static/data/monastery_panoramas.json` - Panoramic image configuration

### Features
- **Dynamic Loading**: Panoramas are loaded from JSON configuration
- **Error Handling**: Graceful fallback when images fail to load
- **Loading States**: Visual feedback during panorama initialization
- **Responsive Design**: Works on desktop and mobile devices
- **Accessibility**: Alt text and proper ARIA labels

### Viewer Configuration
Uses Pannellum.js with the following features:
- Auto-rotation for immersive experience
- Zoom and fullscreen controls
- Mouse/touch navigation
- Keyboard navigation support
- Compass for orientation
- Custom initial viewing angles for each monastery

## Future Enhancements

### Recommended Improvements

1. **Actual 360° Photography**
   - Commission professional 360° photography of each monastery
   - Capture multiple views per monastery (exterior, interior, grounds)
   - Include seasonal variations

2. **Interactive Hotspots**
   - Add clickable information points within panoramas
   - Link to detailed explanations of architectural features
   - Connect to relevant archive materials

3. **Audio Narration**
   - Add guided audio tours for each panoramic view
   - Include monastery history and architectural significance
   - Multi-language support (English, Hindi, Nepali)

4. **Virtual Tours**
   - Connect multiple panoramas for complete monastery walkthrough
   - Floor plans and navigation between different areas
   - Progressive disclosure of information

5. **Real-Time Data**
   - Weather conditions and seasonal changes
   - Festival and ceremony schedules
   - Visitor information and guidelines

## Content Guidelines

### Image Requirements
- **Resolution**: Minimum 4K (4096x2048) for equirectangular images
- **Format**: JPEG or WebP for web optimization
- **Aspect Ratio**: 2:1 for equirectangular projection
- **Quality**: High quality with minimal compression artifacts
- **Content**: Culturally respectful photography with proper permissions

### Metadata Standards
- Proper attribution for all images
- GPS coordinates for mapping integration
- Timestamp for seasonal accuracy
- Cultural and historical context

## Legal Considerations

### Current Images
All current images are sourced from Unsplash under their license terms:
- Free to use for commercial and non-commercial purposes
- No permission needed from Unsplash or photographer
- Attribution appreciated but not required

### Future Content
For actual monastery photography:
- Obtain proper permissions from monastery authorities
- Respect religious and cultural sensitivities
- Follow photography guidelines for sacred spaces
- Ensure visitor and monk privacy

## Usage Instructions

### For Developers
1. Update `/static/data/monastery_panoramas.json` to add new panoramas
2. Include proper metadata and viewing parameters
3. Test panoramic viewer initialization
4. Verify error handling and fallbacks

### For Content Managers
1. Source appropriate panoramic images
2. Configure viewing angles for optimal experience
3. Write descriptive titles and explanations
4. Maintain proper attribution records

---

*Last Updated: September 8, 2025*
*Version: 1.0*

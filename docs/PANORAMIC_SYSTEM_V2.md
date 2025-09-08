# Enhanced Multi-View Panoramic System Documentation

## Overview

The monastery360 project features a comprehensive **multi-view panoramic system** that allows users to explore different areas within each monastery through 360° views with audio narration. This enhanced system provides an immersive virtual tour experience with:

- **Multiple panoramic views per monastery** (e.g., Main Hall, Courtyard, Exterior)
- **Interactive navigation** between different areas
- **Audio narration** for each panoramic view 
- **Hotspot functionality** for points of interest
- **Responsive design** for all devices

## Architecture

### Core Components

1. **JSON Configuration System** (`/static/data/monastery_panoramas.json`)
   - Central configuration file for all monastery panoramic data
   - Supports multiple views per monastery
   - Includes audio files, viewing parameters, and hotspot data

2. **Enhanced React Components** (in Django templates)
   - Multi-view panoramic viewer with navigation controls
   - Audio control system with play/pause functionality
   - View information panels with descriptions
   - Loading states and error handling

3. **Pannellum.js Integration**
   - 360° panoramic image rendering
   - Interactive controls (zoom, rotation, fullscreen)
   - Hotspot support for informational overlays

4. **Audio Narration System**
   - MP3 audio files for each panoramic view
   - Play/pause controls integrated with viewer
   - Audio stops automatically when switching views

## Configuration Structure

### JSON Schema

```json
{
  "monasteries": {
    "monastery_slug": {
      "name": "Monastery Name",
      "views": [
        {
          "id": "unique_view_id",
          "title": "View Title",
          "description": "Detailed description of the view",
          "url": "https://example.com/panorama.jpg",
          "type": "equirectangular",
          "yaw": 0,
          "pitch": -10,
          "hfov": 110,
          "audio": "/static/audio/view_audio.mp3",
          "audioDuration": 45,
          "hotspots": [
            {
              "pitch": -2,
              "yaw": 45,
              "type": "info",
              "text": "Point of Interest",
              "description": "Detailed information about this point"
            }
          ]
        }
      ]
    }
  },
  "defaultView": {
    "title": "Default View",
    "description": "Fallback panoramic view",
    "url": "https://example.com/default.jpg",
    "type": "equirectangular",
    "yaw": 0,
    "pitch": 0,
    "hfov": 110
  }
}
```

### View Properties

- **id**: Unique identifier for the view
- **title**: Display name for navigation buttons
- **description**: Explanatory text shown in view info panel
- **url**: Direct link to equirectangular panoramic image
- **type**: Image projection type (always "equirectangular")
- **yaw**: Horizontal viewing angle (degrees)
- **pitch**: Vertical viewing angle (degrees)
- **hfov**: Horizontal field of view (degrees, affects zoom level)
- **audio**: Path to MP3 narration file
- **audioDuration**: Length of audio in seconds
- **hotspots**: Array of interactive information points

## Implementation Details

### Multi-View Navigation

Each monastery can have multiple panoramic views representing different areas:
- **Main Prayer Hall**: Interior view of the primary worship space
- **Courtyard**: Central gathering area for ceremonies
- **Exterior**: Outside architecture and mountain views
- **Meditation Hall**: Quiet spaces for contemplation
- **Festival Grounds**: Areas used for special celebrations

Users can navigate between views using prominent navigation buttons that appear above the panoramic viewer when multiple views are available.

### Audio Integration

Each panoramic view can have associated audio narration that provides:
- Historical context about the monastery
- Architectural details and significance
- Cultural and religious explanations
- Visitor guidance and points of interest

Audio controls are integrated directly into the viewer interface with:
- Play/pause toggle functionality
- Visual feedback for current playback status
- Automatic audio stopping when switching views
- Duration display for user convenience

### Hotspot System

Interactive hotspots can be placed within panoramic views to highlight:
- Significant architectural features
- Religious artifacts and statues
- Historical elements
- Cultural symbols and decorations

Hotspots appear as clickable markers that display informational overlays when activated.

## Current Implementation Status

### Configured Monasteries

1. **Rumtek Monastery**
   - Main Prayer Hall (45s audio)
   - Monastery Courtyard (38s audio)
   - Monastery Exterior (42s audio)

2. **Pemayangtse Monastery** 
   - Main Prayer Hall (52s audio)
   - Meditation Hall (35s audio)
   - Himalayan View (28s audio)

3. **Enchey Monastery**
   - Prayer Hall with Murals (48s audio)
   - Cham Dance Ground (33s audio)

### Audio Files

Audio files are located at `/static/audio/` with the following naming convention:
- `{monastery}_{view}.mp3`
- Example: `rumtek_main_hall.mp3`

**Note**: Current audio files are placeholder tones. Replace with professional narration for production use.

## Usage Instructions

### Adding New Monasteries

1. **Add monastery entry** to `monastery_panoramas.json`:
```json
"new_monastery": {
  "name": "New Monastery Name",
  "views": [
    {
      "id": "new_monastery_main_hall",
      "title": "Main Hall",
      "description": "Description of the main hall",
      "url": "https://your-image-url.jpg",
      "type": "equirectangular",
      "yaw": 0,
      "pitch": 0,
      "hfov": 110,
      "audio": "/static/audio/new_monastery_main_hall.mp3",
      "audioDuration": 60
    }
  ]
}
```

2. **Create audio files** in `/static/audio/` directory
3. **Update Django models** if necessary to include new monastery slug
4. **Test functionality** across all devices and browsers

### Adding New Views to Existing Monasteries

1. **Extend views array** in monastery configuration
2. **Source high-quality equirectangular images** (preferably 4K+ resolution)
3. **Create corresponding audio narration**
4. **Set optimal viewing parameters** (yaw, pitch, hfov)
5. **Add relevant hotspots** for points of interest

## Technical Considerations

### Performance Optimization

- **Image Optimization**: Use compressed, web-optimized equirectangular images
- **Lazy Loading**: Pannellum loads images on-demand
- **Audio Preloading**: Audio files are loaded when view is selected
- **Caching**: Implement browser caching for static assets

### Browser Compatibility

- **Modern Browsers**: Full support for Chrome, Firefox, Safari, Edge
- **Mobile Devices**: Responsive design with touch controls
- **WebGL**: Enhanced performance on WebGL-capable browsers
- **Fallbacks**: Graceful degradation for older browsers

### Image Requirements

- **Format**: JPEG recommended for file size efficiency
- **Projection**: Equirectangular (360° x 180°)
- **Resolution**: Minimum 2048x1024, recommended 4096x2048 or higher
- **Aspect Ratio**: Exactly 2:1 (width:height)
- **Quality**: High quality with minimal compression artifacts

## Future Enhancements

### Planned Features

1. **Professional Photography**: Commission actual 360° monastery photography
2. **Interactive Guided Tours**: Step-by-step walkthrough functionality
3. **VR Headset Support**: WebVR/WebXR integration
4. **Multi-language Audio**: Narration in multiple languages
5. **Historical Timeline Views**: Show monastery changes over time
6. **Social Sharing**: Share specific views and moments
7. **Accessibility Features**: Screen reader support, keyboard navigation

### Advanced Functionality

- **Dynamic Hotspot Loading**: Load hotspots from external API
- **User-Generated Content**: Allow visitors to contribute information
- **Analytics Integration**: Track popular views and engagement
- **Offline Support**: Cache panoramas for offline viewing
- **AI-Powered Descriptions**: Automatic generation of view descriptions

## Maintenance

### Regular Tasks

- **Update Image Quality**: Replace images with higher resolution versions
- **Refresh Audio Content**: Update narration with new information
- **Monitor Performance**: Check loading times and user experience
- **Validate Links**: Ensure all image URLs remain accessible
- **Backup Configuration**: Regular backups of JSON configuration

### Troubleshooting

- **Images Not Loading**: Check URL accessibility and CORS policies
- **Audio Playback Issues**: Verify MP3 file format and browser support
- **Performance Problems**: Optimize image sizes and implement lazy loading
- **Mobile Issues**: Test touch controls and responsive layouts

## Legal and Attribution

### Image Rights

- **Source**: High-quality images from Unsplash with proper attribution
- **License**: Unsplash License allows commercial and non-commercial use
- **Attribution**: Credit information included in configuration metadata
- **Replacement**: Consider commissioning original photography for production

### Audio Content

- **Narration**: Create original audio content to avoid copyright issues
- **Background Music**: Use royalty-free music if desired
- **Voice Actors**: Consider professional narration for quality enhancement

---

*This documentation reflects the enhanced multi-view panoramic system with audio narration capabilities. Update this document as new features are implemented.*

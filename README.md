# all-is-all
A minimalist showcase for all my digital projects and experiments.

## Features

- Clean, minimalist design
- Mobile-friendly responsive layout
- Two view modes (desktop only):
  - Grid view: Card-based layout
  - List view: Table-like layout
- Project tagging system
- No build tools required
- Easy configuration through web interface

## Usage

1. Fork this repository
2. Access `/config` to manage your projects
3. Edit projects:
   - Add/Edit/Delete projects
   - Drag to reorder
   - Add tags
4. Download the updated `projects.json`
5. Commit and deploy

## Structure

```
all-is-all/
├── index.html    # Main showcase page
├── config.html   # Project management interface
└── projects.json # Project data
```

## Customization

Edit `projects.json` directly or use the config interface at `/config` to manage your projects. Each project entry includes:

```json
{
  "name": "Project Name",
  "url": "project.example.com",
  "description": "Project description",
  "tags": ["tag1", "tag2"]
}
```

## License

MIT

# NaukriAI Dashboard

A modern, responsive recruitment dashboard built with React, TypeScript, and Tailwind CSS. Features AI-powered candidate search, advanced matching algorithms, and intelligent CV analysis.

## Features

### 🎯 Core Functionality
- **Dashboard Analytics**: Interactive charts showing skill distribution, seniority levels, experience ranges, and employment types
- **AI-Powered Search**: Natural language candidate search with intelligent matching
- **Advanced Matching**: Multi-criteria candidate filtering with skill requirements, experience, and preferences
- **CV Analyzer**: Automated resume parsing and candidate profiling

### 🎨 Design & UX
- **Monochrome Theme**: Professional black and white design with subtle gray accents
- **Responsive Design**: Optimized for mobile, tablet, and desktop viewing
- **Dark/Light Mode**: Toggle between themes with persistent user preference
- **Smooth Animations**: Micro-interactions and loading states for enhanced UX
- **Collapsible Sidebar**: Space-efficient navigation that collapses on mobile

### 🛠 Technical Stack
- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS with custom design system
- **Charts**: Recharts for data visualization
- **HTTP Client**: Axios with interceptors for API calls
- **State Management**: TanStack Query for server state and caching
- **Routing**: React Router v6
- **File Upload**: React Dropzone for CV uploads
- **Icons**: Lucide React

## Project Structure

```
src/
├── components/
│   ├── Layout/           # App layout components
│   ├── Dashboard/        # Chart components
│   ├── AISearch/         # Search functionality
│   ├── AdvancedMatch/    # Matching system
│   ├── CVAnalyzer/       # CV analysis components
│   └── common/           # Reusable UI components
├── pages/                # Main page components
├── api/                  # API client and endpoints
├── hooks/                # Custom React hooks
├── types/                # TypeScript type definitions
└── App.tsx              # Main application component
```

## API Integration

The application integrates with the following REST API endpoints:

- `GET /dataset/top-skills?top_n=n` - Fetch top skills data
- `GET /dataset/seniority-distribution` - Get seniority level distribution
- `GET /dataset/experience-distribution` - Get experience range distribution
- `GET /dataset/employment-type-distribution` - Get employment type data
- `GET /dataset/skills-by-seniority/{seniority}` - Skills by seniority level
- `POST /search-candidates` - AI-powered candidate search
- `POST /advanced-match` - Advanced candidate matching
- `POST /analyze-cv` - CV analysis and parsing

## Getting Started

### Prerequisites
- Node.js 18+ and npm

### Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Set up environment variables**:
Create a `.env` file in the root directory:
```env
VITE_API_URL=http://localhost:8000
```

3. **Start the development server**:
```bash
npm run dev
```

4. **Build for production**:
```bash
npm run build
```

### Development Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run test` - Run tests with Vitest

## Key Features in Detail

### Dashboard Analytics
Interactive charts powered by Recharts showing:
- Top in-demand skills with candidate counts
- Seniority level distribution (pie chart)
- Experience range distribution (area chart)
- Employment type breakdown (bar chart)

### AI Search
- Natural language query processing
- Intelligent candidate matching
- Real-time search results with scoring
- Candidate profile cards with key information

### Advanced Matching
- Multi-step form for detailed criteria
- Required vs. preferred skills distinction
- Experience and seniority filtering
- Expandable results with match scores
- Customizable result limits

### CV Analyzer
- Drag-and-drop file upload
- Support for PDF, DOC, and DOCX formats
- Automated information extraction
- Comprehensive candidate profiles
- Skill identification and categorization

## Design System

### Color Palette
- **Primary**: Shades of gray from #f8fafc to #0f172a
- **Accent**: Professional monochrome with subtle variations
- **Status Colors**: Minimal color usage for success/warning/error states

### Typography
- **Headings**: Bold, clear hierarchy
- **Body**: Readable with proper line spacing
- **Code**: Monospace for technical content

### Spacing
- **8px Grid System**: Consistent spacing throughout
- **Responsive Breakpoints**: Mobile-first approach
- **Container Sizes**: Optimal content width on all devices

## Performance Optimizations

- **React Query Caching**: Server state management with automatic background updates
- **Code Splitting**: Route-based lazy loading
- **Image Optimization**: Proper sizing and lazy loading
- **Bundle Optimization**: Tree shaking and minification
- **API Caching**: 5-minute stale time for dashboard data

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and commit: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Deployment

The application builds to static files and can be deployed to any CDN or static hosting service:

- **Netlify**: Connect your repository for automatic deployments
- **Vercel**: Import project for seamless deployment
- **AWS S3 + CloudFront**: Upload build files to S3 bucket
- **GitHub Pages**: Use GitHub Actions for automated deployment

Build command: `npm run build`
Output directory: `dist/`

## Support

For support and questions, please open an issue in the GitHub repository or contact the development team.
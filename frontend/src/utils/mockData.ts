import { 
  Skill, 
  SeniorityDistribution, 
  ExperienceDistribution, 
  EmploymentTypeDistribution,
  Candidate,
  CVAnalysisResult 
} from '../types/api';

// Mock data for when API is unavailable
export const mockSkills: Skill[] = [
  { name: 'JavaScript', count: 1250, percentage: 25.5 },
  { name: 'React', count: 980, percentage: 20.0 },
  { name: 'Python', count: 875, percentage: 17.8 },
  { name: 'Node.js', count: 720, percentage: 14.7 },
  { name: 'TypeScript', count: 650, percentage: 13.2 },
  { name: 'Java', count: 580, percentage: 11.8 },
  { name: 'SQL', count: 520, percentage: 10.6 },
  { name: 'AWS', count: 480, percentage: 9.8 },
  { name: 'Docker', count: 420, percentage: 8.6 },
  { name: 'GraphQL', count: 350, percentage: 7.1 },
];

export const mockSeniorityDistribution: SeniorityDistribution[] = [
  { seniority: 'Junior', count: 1200, percentage: 30.0 },
  { seniority: 'Mid-level', count: 1600, percentage: 40.0 },
  { seniority: 'Senior', count: 800, percentage: 20.0 },
  { seniority: 'Lead', count: 300, percentage: 7.5 },
  { seniority: 'Principal', count: 100, percentage: 2.5 },
];

export const mockExperienceDistribution: ExperienceDistribution[] = [
  { experience_range: '0-2 years', count: 800, percentage: 20.0 },
  { experience_range: '2-5 years', count: 1200, percentage: 30.0 },
  { experience_range: '5-8 years', count: 1000, percentage: 25.0 },
  { experience_range: '8-12 years', count: 600, percentage: 15.0 },
  { experience_range: '12+ years', count: 400, percentage: 10.0 },
];

export const mockEmploymentTypeDistribution: EmploymentTypeDistribution[] = [
  { employment_type: 'Full-time', count: 2800, percentage: 70.0 },
  { employment_type: 'Contract', count: 800, percentage: 20.0 },
  { employment_type: 'Part-time', count: 280, percentage: 7.0 },
  { employment_type: 'Freelance', count: 120, percentage: 3.0 },
];

export const mockCandidates: Candidate[] = [
  {
    id: '1',
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    skills: ['React', 'TypeScript', 'Node.js', 'GraphQL', 'AWS'],
    experience_years: 5,
    seniority: 'Senior',
    employment_type: 'Full-time',
    score: 0.92,
    summary: 'Experienced full-stack developer with expertise in modern web technologies and cloud platforms.',
  },
  {
    id: '2',
    name: 'Michael Chen',
    email: 'michael.chen@email.com',
    skills: ['Python', 'Django', 'PostgreSQL', 'Docker', 'Kubernetes'],
    experience_years: 7,
    seniority: 'Senior',
    employment_type: 'Full-time',
    score: 0.88,
    summary: 'Backend specialist with strong experience in Python ecosystem and DevOps practices.',
  },
  {
    id: '3',
    name: 'Emily Rodriguez',
    email: 'emily.rodriguez@email.com',
    skills: ['JavaScript', 'Vue.js', 'CSS', 'HTML', 'Figma'],
    experience_years: 3,
    seniority: 'Mid-level',
    employment_type: 'Full-time',
    score: 0.85,
    summary: 'Frontend developer with a keen eye for design and user experience.',
  },
];

export const mockCVAnalysis: CVAnalysisResult = {
  name: 'John Doe',
  email: 'john.doe@email.com',
  phone: '+1 (555) 123-4567',
  skills: ['React', 'TypeScript', 'Node.js', 'MongoDB', 'Express.js', 'Jest', 'Git'],
  experience_years: 4,
  seniority: 'Mid-level',
  summary: 'Passionate full-stack developer with 4 years of experience building scalable web applications. Strong background in React ecosystem and modern JavaScript development practices.',
  education: [
    'Bachelor of Science in Computer Science - University of Technology (2019)',
    'Full Stack Web Development Bootcamp - Tech Academy (2020)'
  ],
  certifications: [
    'AWS Certified Developer Associate',
    'MongoDB Certified Developer'
  ],
  score: 78,
};

// Utility function to simulate API delay
export const simulateApiDelay = (ms: number = 1000): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};
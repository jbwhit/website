## TODO List for Quarto Website Migration

### Context for Claude Code

**Goal:** Migrate from nbdev-based website to a clean Quarto website inspired by Mickaël Canouil's aesthetic (https://mickael.canouil.fr)

**Current state:** Working on branch `quarto-redesign` in the existing repo

**Design inspiration:** Clean, minimal aesthetic with clear navigation sections

**Key requirements:**
- Preserve all existing content (blog posts, checklists, physics quals)
- Enable Jupyter notebook integration for future posts
- Maintain custom domain (jonathanwhitmore.com) - CNAME file goes in root
- Use GitHub Pages for hosting

---

## Step-by-Step Tasks

### 1. Initialize Quarto Website Structure

- [ ] Create basic Quarto website structure in the root directory (we're working in a branch, so it's safe to overwrite)
- [ ] Create `_quarto.yml` with the following structure:
  - Website title: "Jonathan Whitmore"
  - Navbar with sections: Home, Blog, Projects, About
  - Clean theme (use Mickaël's as inspiration: likely cosmo or flatly with custom SCSS)
  - Enable blog listings with categories/tags
  - Set up proper output directory for GitHub Pages

### 2. Create Directory Structure

Create the following directories:
```
├── posts/                    # Blog posts go here
├── projects/                 # Projects section
│   ├── checklists/          # Checklists subsection
│   └── physics-quals/       # Physics quals subsection
├── assets/
│   └── images/              # Images and media
└── CNAME                    # Custom domain file (jonathanwhitmore.com)
```

### 3. Create Core Pages

- [ ] `index.qmd` - Home/About page with brief bio
- [ ] `blog.qmd` - Blog listing page
- [ ] `projects.qmd` - Projects landing page (optional, or use navbar dropdown)
- [ ] `about.qmd` - Detailed about page (or merge with index.qmd)

### 4. Migrate Blog Posts

Move and convert existing blog posts to the new structure:

**Post 1: MathAcademy Review**
- [ ] Create `posts/2024-09-10-mathacademy/index.qmd`
- [ ] Convert from `nbs/posts/2024-09-10-MathAcademy-after-2000-points/index.qmd`
- [ ] Copy associated images to post directory
- [ ] Update frontmatter for Quarto blog format

**Post 2: CNAME GitHub Pages Fix**
- [ ] Create `posts/2024-07-11-cname-fix/index.qmd`
- [ ] Convert from `nbs/posts/2024-07-11-cname-github-pages/index.qmd`
- [ ] Copy images
- [ ] Update frontmatter

**Post 3: Misusing Machine Learning**
- [ ] Create `posts/2023-12-19-ml/index.qmd`
- [ ] Convert from `nbs/posts/2023-12-19-misusing-machine-learning/index.ipynb`
- [ ] Copy images/GIFs
- [ ] Ensure embedded video works
- [ ] Update frontmatter

### 5. Migrate Checklists

- [ ] Create `projects/checklists/index.qmd` - Landing page for checklists
- [ ] Create `projects/checklists/investing.qmd` from `nbs/checklists/investing.qmd`
- [ ] Create `projects/checklists/did.qmd` from `nbs/checklists/difference-in-differences.qmd`
- [ ] Keep markdown downloads available (investment_checklist.md, did_checklist.md)

### 6. Migrate Physics Quals

- [ ] Create `projects/physics-quals/index.qmd` from `nbs/physics/physics-quals/index.qmd`
- [ ] Ensure all Dropbox links still work
- [ ] Consider structure: keep as single page or break into sections?

### 7. Configuration & Styling

- [ ] Set up `_quarto.yml` with:
  - Proper site URL (https://jonathanwhitmore.com)
  - Blog listings configuration
  - Navigation structure
  - Theme customization (consider creating custom.scss)
  - Social links (Twitter/X, LinkedIn, YouTube, GitHub)
  - RSS feed for blog

- [ ] Create `CNAME` file in root with: `jonathanwhitmore.com`

- [ ] Create `.gitignore` appropriate for Quarto:
```
/.quarto/
/_site/
```

### 8. GitHub Actions for Deployment

- [ ] Create `.github/workflows/publish.yml` for automated deployment to GitHub Pages
- [ ] Configure to deploy to `gh-pages` branch or docs folder
- [ ] Test deployment workflow

### 9. Testing & Cleanup

- [ ] Test local rendering: `quarto preview`
- [ ] Verify all internal links work
- [ ] Check all images display correctly
- [ ] Ensure CNAME is in the right place for deployment
- [ ] Test navigation on mobile (responsive design)
- [ ] Verify RSS feed works

### 10. Content Polish

- [ ] Review and update `index.qmd` with current bio/intro
- [ ] Ensure consistent formatting across all posts
- [ ] Add categories/tags to blog posts for better discovery
- [ ] Consider adding a site favicon

---

## Key Files to Reference

From current nbdev setup:
- `nbs/_quarto.yml` - Current Quarto config
- `nbs/sidebar.yml` - Current navigation structure
- `settings.ini` - Site metadata (author, description, etc.)

## Important Notes

1. **CNAME file location**: Place in root directory (not in `nbs/` like before)
2. **Blog post format**: Use Quarto's blog format with proper frontmatter (title, description, author, date, categories)
3. **Jupyter notebooks**: Quarto natively supports `.ipynb` files - can include them directly in posts/
4. **Custom domain**: Ensure GitHub Pages settings point to custom domain after deployment

## Success Criteria

- [ ] Site renders locally with `quarto preview`
- [ ] All existing content is accessible at intuitive URLs
- [ ] Blog posts display correctly with listings
- [ ] Custom domain works (jonathanwhitmore.com)
- [ ] Site is visually clean and professional (Mickaël-inspired aesthetic)
- [ ] Mobile-responsive design
- [ ] Fast loading times

---

**Additional Context:**
- User prefers plain-text workflows
- Wants ability to embed Jupyter notebooks with code/output
- Physics background (PhD candidate, taught at UCSD)
- Interests in learning systems, ML, data analysis, investing
- Writing style: technical but accessible, occasional humor

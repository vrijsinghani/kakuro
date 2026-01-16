import { useState } from 'react';
import { BookOpen, Brain, Coffee, Leaf, Star, CheckCircle2, ArrowRight, X, Zap, Activity, TrendingUp } from 'lucide-react';
import coverImage from './assets/cover_front.jpg';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function App() {
  const [showPreview, setShowPreview] = useState(false);

  return (
    <div className="min-h-screen flex flex-col font-sans text-forest">
      {/* Decorative top bar */}
      <div className="h-2 bg-gradient-to-r from-sage via-cream to-sage" />

      {/* Hero Section */}
      <section className="px-4 pt-16 pb-12 overflow-hidden relative">
        {/* Background blobs */}
        <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-sage/20 rounded-full blur-3xl -z-10 animate-pulse"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-[400px] h-[400px] bg-bronze/10 rounded-full blur-3xl -z-10"></div>

        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8 text-center md:text-left order-2 md:order-1">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-bronze/10 text-bronze-dark text-sm font-semibold tracking-wide border border-bronze/20">
                <Leaf className="w-4 h-4 text-bronze-dark" />
                <span>Newly Released</span>
              </div>
              <h1 className="text-5xl md:text-7xl font-serif font-bold text-forest leading-[1.1] text-shadow-sm">
                Master <span className="text-bronze">Kakuro</span>
              </h1>
              <p className="text-xl md:text-2xl text-forest/80 font-medium font-serif italic">
                Relaxing Logic Puzzles for a Sharp Mind
              </p>
              <p className="text-lg text-forest/70 max-w-lg mx-auto md:mx-0 leading-relaxed">
                Disconnect from screens and reconnect with your focus. 250 handcrafted puzzles designed to calm the mind and strengthen cognitive resilience.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
              <a
                href="https://a.co/d/2NnLQW7"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-4 bg-bronze hover:bg-bronze-dark text-white rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 transform hover:-translate-y-1"
              >
                Buy on Amazon <ArrowRight className="w-5 h-5" />
              </a>
              <button
                onClick={() => setShowPreview(true)}
                className="px-8 py-4 bg-cream border-2 border-bronze text-bronze-dark hover:bg-bronze/5 rounded-full font-semibold text-lg transition-all flex items-center justify-center gap-2"
              >
                Look Inside <BookOpen className="w-5 h-5" />
              </button>
            </div>

            <div className="pt-4 flex items-center justify-center md:justify-start gap-6 text-sm font-medium text-forest/60">
              <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-bronze" /> Volume 1</span>
              <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-bronze" /> Large Print</span>
            </div>
          </div>

          {/* Right Content - Book Cover */}
          <div className="flex justify-center md:justify-end relative group perspective-1000 order-1 md:order-2">
            {/* 3D Book Cover Effect */}
            <div className="relative w-full max-w-md transform transition-transform duration-500 ease-out group-hover:rotate-y-6 preserve-3d">
              <img
                src={coverImage}
                alt="Master Kakuro Book Cover"
                className="w-full rounded-r-xl rounded-l-sm shadow-2xl book-shadow relative z-10"
              />
              {/* Book Spine Simulation */}
              <div className="absolute top-1 bottom-1 left-0 w-4 bg-gradient-to-r from-gray-800 to-gray-600 transform -translate-x-3 translate-z-[-10px] rotate-y-[-90deg] origin-right rounded-l-sm"></div>
            </div>

            {/* Floating Badge */}
            <div className="absolute -top-6 -right-6 md:right-0 bg-bronze text-white w-24 h-24 rounded-full flex flex-col items-center justify-center shadow-lg animate-bounce-slow z-20">
              <span className="text-2xl font-bold font-serif leading-none">250</span>
              <span className="text-xs uppercase tracking-wide font-medium">Puzzles</span>
            </div>
          </div>
        </div>
      </section>

      {/* Preview Modal */}
      {showPreview && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-forest/80 backdrop-blur-sm animate-in fade-in duration-200" onClick={() => setShowPreview(false)}>
          <div className="relative max-w-2xl w-full bg-white rounded-xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-cream/30">
              <h3 className="text-xl font-serif font-bold text-forest">Interior Preview (Page 54)</h3>
              <button
                onClick={() => setShowPreview(false)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors text-gray-500 hover:text-red-500"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="p-0 bg-gray-50 max-h-[80vh] overflow-auto flex justify-center">
              <img
                src="/preview_page_54.png"
                alt="Book Interior Preview - Page 54"
                className="max-w-full shadow-lg"
              />
            </div>
            <div className="p-4 border-t border-gray-100 bg-white flex justify-end">
              <button
                onClick={() => setShowPreview(false)}
                className="px-6 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Benefits / Features */}
      <section className="py-24 bg-white relative">
        <div className="container mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <h2 className="text-3xl md:text-5xl font-serif font-bold text-forest">Focus, Logic, Calm</h2>
            <p className="text-lg text-forest/70 leading-relaxed">
              Kakuro combines the pure logic of Sudoku with simple arithmetic. It’s the perfect ritual to start your morning or unwind at night.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <FeatureCard
              icon={Brain}
              title="Cognitive Sharpness"
              desc="Strengthens logical reasoning and mental math skills through active problem solving."
            />
            <FeatureCard
              icon={Coffee}
              title="Daily Ritual"
              desc="A consistent, quiet habit that centers your mind before or after a busy digital day."
            />
            <FeatureCard
              icon={Leaf}
              title="Screen-Free"
              desc="Physical paper and pencil. No notifications, no blue light, just pure focus."
            />
            <FeatureCard
              icon={Star}
              title="Mastery Path"
              desc="Start simple and grow. Our carefully curated difficulty curve guides you to expertise."
            />
          </div>
        </div>
      </section>

      {/* Science of Solving Section */}
      <section className="py-24 bg-forest text-cream relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-sage/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center mb-16 space-y-4">
            <h2 className="text-3xl md:text-5xl font-serif font-bold">The Science of Solving</h2>
            <p className="text-xl text-cream/70 italic">
              Research consistently links logic puzzles to better cognitive health. Kakuro delivers this brain-training in its purest form.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            <div className="space-y-8">
              <ScienceCard
                icon={TrendingUp}
                title="Delay Memory Decline"
                desc="A 2011 study found frequent puzzle solvers delayed the onset of accelerated memory decline by 2.5 years compared to non-puzzlers.¹"
              />
              <ScienceCard
                icon={Activity}
                title="Younger Brain Function"
                desc="The extensive PROTECT study found that those who regularly solve word and number puzzles have brain function equivalent to up to 10 years younger.²"
              />
            </div>
            <div className="space-y-8">
              <ScienceCard
                icon={Zap}
                title="Larger Brain Volume"
                desc="Cognitively stimulating activities like games and puzzles are associated with larger brain volumes and better cognitive abilities in older adults.³"
              />
              <ScienceCard
                icon={Coffee}
                title="Dopamine-Driven Focus"
                desc='The "Aha!" moment of solving a difficult row releases dopamine, naturally boosting mood, memory, and concentration.'
              />
            </div>
          </div>

          <div className="mt-16 text-xs text-cream/40 px-4 max-w-3xl mx-auto text-left space-y-2 font-mono">
            <p className="font-bold text-cream/60 mb-2 uppercase tracking-wider">Scientific References</p>
            <p>1. Verghese et al., "Association of Crossword Puzzle Participation with Memory Decline in Persons who Develop Dementia," <em>J Int Neuropsychol Soc.</em> 2011. <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3885259/" target="_blank" rel="noopener noreferrer" className="underline hover:text-cream/80">View Study</a></p>
            <p>2. Corbett et al., University of Exeter & King's College London PROTECT Study, 2019. <a href="https://www.exeter.ac.uk/news/featurednews/title_716265_en.html" target="_blank" rel="noopener noreferrer" className="underline hover:text-cream/80">View News Release</a></p>
            <p>3. Schultz et al., "Participation in Cognitively-Stimulating Activities is Associated with Brain Structure and Cognitive Function in Preclinical Alzheimer's Disease," <em>Brain Imaging Behav.</em> 2015. <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4417099/" target="_blank" rel="noopener noreferrer" className="underline hover:text-cream/80">View Study</a></p>
          </div>
        </div>
      </section>

      {/* What's Inside - Split Layout */}
      <section id="preview" className="py-24 bg-sage/10 relative overflow-hidden">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-12 gap-12 items-center">
            <div className="md:col-span-5 relative group cursor-pointer" onClick={() => setShowPreview(true)}>
              <div className="aspect-[3/4] bg-white rounded-lg shadow-2xl p-8 border border-stone/10 rotate-2 transition-transform duration-300 group-hover:rotate-0 group-hover:scale-105">
                {/* Abstract Puzzle Visualization */}
                <div className="w-full h-full border-2 border-forest/80 opacity-20 p-4 grid grid-cols-6 gap-0">
                  {Array.from({ length: 36 }).map((_, i) => <div key={i} className={cn("border border-forest/80", i % 3 === 0 && "bg-forest/80")}></div>
                  )}
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="bg-forest text-cream px-4 py-2 rounded-full text-sm font-medium shadow-lg hover:bg-forest/90 transition-colors">Preview Page 54</span>
                </div>
              </div>
              {/* Decorative card behind */}
              <div className="absolute inset-0 bg-sage-dark rounded-lg -rotate-3 -z-10 translate-x-4 translate-y-4 opacity-20"></div>
            </div>

            <div className="md:col-span-7 space-y-8">
              <h2 className="text-3xl md:text-5xl font-serif font-bold text-forest">A Premium Collection</h2>
              <div className="space-y-6">
                <CheckItem title="Algorithmically Verified" desc="Every puzzle is generated using intelligent problem-solving methods to guarantee a single, unique solution. No guessing required." />
                <CheckItem title="Large Print Format" desc="Easy on the eyes with spacious 8.5x11 layout and clear typography." />
                <CheckItem title="Guided Progression" desc="75 Beginner, 95 Intermediate, and 80 Expert puzzles to build your skills." />
                <CheckItem title="Full Solutions" desc="Complete solutions at the back—never get stuck without a way forward." />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA / Footer */}
      <footer className="mt-auto bg-forest py-20 text-cream relative overflow-hidden">
        <div className="absolute inset-0 bg-noise opacity-10 mix-blend-overlay"></div>
        <div className="container mx-auto px-6 text-center relative z-10">
          <h2 className="text-4xl md:text-5xl font-serif font-bold mb-8 text-cream">Ready to Master Kakuro?</h2>
          <p className="text-xl text-cream/80 mb-10 max-w-2xl mx-auto">
            Order your copy today and rediscover the joy of analog puzzle solving.
          </p>
          <a
            href="https://a.co/d/2NnLQW7"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-3 bg-bronze text-forest font-bold px-10 py-4 rounded-xl shadow-lg hover:bg-bronze-dark hover:text-white hover:-translate-y-1 transition-all duration-300"
          >
            <span>Get it on Amazon</span>
            <ArrowRight className="w-5 h-5" />
          </a>

          <div className="mt-20 pt-10 border-t border-white/10 text-sm text-white/40 flex flex-col md:flex-row justify-between items-center gap-4">
            <p>© 2026 Master Kakuro Series. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="#" className="hover:text-bronze transition-colors">Privacy</a>
              <a href="#" className="hover:text-bronze transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Components

function FeatureCard({ icon: Icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <div className="p-8 rounded-2xl bg-sage/5 hover:bg-white border border-transparent hover:border-sage/20 transition-all duration-300 hover:shadow-xl group">
      <div className="w-12 h-12 bg-cream rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
        <Icon className="w-6 h-6 text-forest" />
      </div>
      <h3 className="text-xl font-serif font-bold text-forest mb-3">{title}</h3>
      <p className="text-forest/70 leading-relaxed text-sm">{desc}</p>
    </div>
  )
}

function ScienceCard({ icon: Icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <div className="flex gap-6 items-start p-6 rounded-2xl bg-white/5 hover:bg-white/10 transition-colors border border-white/10">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-bronze/20 flex items-center justify-center">
        <Icon className="w-6 h-6 text-bronze" />
      </div>
      <div className="space-y-2">
        <h3 className="text-xl font-bold text-cream">{title}</h3>
        <p className="text-cream/60 leading-relaxed">{desc}</p>
      </div>
    </div>
  )
}

function CheckItem({ title, desc }: { title: string, desc: string }) {
  return (
    <div className="flex gap-4 items-start">
      <div className="flex-shrink-0 mt-1">
        <div className="w-6 h-6 rounded-full bg-bronze/10 flex items-center justify-center">
          <CheckCircle2 className="w-4 h-4 text-bronze-dark" />
        </div>
      </div>
      <div>
        <h4 className="font-bold text-forest text-lg mb-1">{title}</h4>
        <p className="text-forest/70 leading-relaxed">{desc}</p>
      </div>
    </div>
  )
}

export default App

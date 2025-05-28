
"""
Optimized main entry point for the TS EAMCET 2025 College Predictor application.
Performance-focused implementation with caching, lazy loading, and session state management.
"""
import streamlit as st
import logging
import pytz
import time
import psutil
import os
from datetime import datetime
from functools import lru_cache
from typing import Optional, Dict, Any, Tuple


# This allows both local and Railway deployment
port = int(os.environ.get("PORT", 8501))
# ============================================================================
# PERFORMANCE MONITORING & LOGGING CONFIGURATION
# ============================================================================

# Configure logging for production (reduced verbosity)
logging.basicConfig(
    level=logging.WARNING if os.getenv(
        'STREAMLIT_ENV') == 'production' else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Performance monitoring utilities"""

    @staticmethod
    def start_monitoring() -> Dict[str, Any]:
        """Start performance monitoring"""
        try:
            start_time = time.time()
            memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            cpu_percent = psutil.cpu_percent(interval=0.1)

            return {
                'start_time': start_time,
                'memory_mb': memory_usage,
                'cpu_percent': cpu_percent
            }
        except Exception:
            return {'start_time': time.time(), 'memory_mb': 0, 'cpu_percent': 0}

    @staticmethod
    def log_performance(metrics: Dict[str, Any], operation_name: str):
        """Log performance metrics if concerning"""
        duration = time.time() - metrics['start_time']

        # Only log performance issues
        if duration > 2.0 or metrics['memory_mb'] > 500:
            logger.warning(
                f"{operation_name}: {duration:.2f}s, {metrics['memory_mb']:.1f}MB, {metrics['cpu_percent']:.1f}% CPU")

        # Show debug metrics in sidebar if enabled
        if st.session_state.get('show_debug_metrics', False):
            with st.sidebar:
                st.metric("⏱️ Load Time", f"{duration:.2f}s")
                st.metric("💾 Memory", f"{metrics['memory_mb']:.1f}MB")
                st.metric("🔧 CPU", f"{metrics['cpu_percent']:.1f}%")

# ============================================================================
# OPTIMIZED DATA LOADING WITH ADVANCED CACHING
# ============================================================================


@st.cache_data(ttl=3600, show_spinner="🔄 Loading college data...")
def load_colleges_data():
    """Load and cache college data with error handling"""
    try:
        from modules.data_loader import load_data
        data = load_data("Final Phase")
        if data is None:
            logger.error("Data loader returned None")
            return None
        logger.info("College data loaded successfully")
        return data
    except ImportError as e:
        logger.error(f"Failed to import data_loader module: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading college data: {e}")
        return None


@st.cache_data(ttl=7200)  # Cache for 2 hours
def get_top_colleges_data() -> Tuple[list, list]:
    """Cache top colleges lists"""
    try:
        from modules.constants import TOP_COLLEGES, TOP_COLLEGES__MALES
        return TOP_COLLEGES, TOP_COLLEGES__MALES
    except ImportError as e:
        logger.error(f"Failed to import constants: {e}")
        return [], []


@st.cache_data(ttl=60)  # Cache for 1 minute to avoid constant time updates
def get_current_time_ist() -> str:
    """Get current IST time (cached)"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime("%I:%M %p IST on %A, %B %d, %Y")


# Optional: Add BuyMeACoffee Button
    # st.markdown(
    # """
    #     <a href="https://www.buymeacoffee.com/bandatharun74" target="_blank">
    #         <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" height="60">
    #     </a>
    #     """,
    #     unsafe_allow_html=True,
    # )

@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_static_content() -> Dict[str, str]:
    """Cache all static content"""
    return {
        'footer_tharun': """
        ### 👨‍💻 MADE BY
        **Tharun**  
        [![GitHub](https://img.shields.io/badge/GitHub-THARUN7474-black?logo=github)](https://github.com/THARUN7474)
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-Banda%20Tharun-blue?logo=linkedin)](https://www.linkedin.com/in/banda-tharun-47b489214)
        [![Twitter](https://img.shields.io/badge/Twitter-BandaTharun7-1da1f2?logo=twitter)](https://x.com/BandaTharun7/)
        [![YouTube](https://img.shields.io/badge/YouTube-BandaTharun-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@banatharun_74)
        """,
        'footer_goutham': """
        ### 🙎‍♂️ With Support
        **Goutham**  
        [![Instagram](https://img.shields.io/badge/Instagram-gouthamsankeerth-purple?logo=instagram)](https://instagram.com/gouthamsankeerth)
        [![YouTube](https://img.shields.io/badge/YouTube-LearnwithGoutham-red?logo=youtube)](https://www.youtube.com/@LearnwithGoutham)
        [![Telegram](https://img.shields.io/badge/Telegram-gouthamsankeerth-2CA5E0?logo=telegram)](https://t.me/careerguidance_gouthamsankeerth)
        """,
        'help_content': """
        ### 📌 Disclaimer
        This tool is based on the **TS EAMCET 2024 cutoff ranks** published in the TGEAPCET 2024 Last Rank Statement.
        
        #### How to Use This Tool
        1. **College Predictor Tab**: Enter rank, gender, category, and preferred branch
        2. **Web Options Generator**: Get strategic college-branch combinations
        3. **College Search**: Find colleges by branch or location
        """,
        'support_message': """
        #### ☕ Support Tharun's Work 
        If you found this tool helpful, consider supporting me on [RazorPay](https://razorpay.me/@your-razorpay-id)! 
        Your support helps me keep building and maintaining tools like this ❤️

        """,
        'social_links': """
        📚 **Find More Student Content:**
        [![LearnwithGoutham](https://img.shields.io/badge/LearnwithGoutham-darkred?logo=youtube)](https://www.youtube.com/@LearnwithGoutham) 
        [![Goutham](https://img.shields.io/badge/Goutham-purple?logo=instagram)](https://instagram.com/gouthamsankeerth) 
        [![Tharun](https://img.shields.io/badge/Tharun-darkorange?logo=youtube)](https://www.youtube.com/@banatharun_74)
        """,
        'disclaimer_content': """
        ⚠️ **Disclaimer**  
        This is a **strategy reference tool**, not a guaranteed admission predictor.
        - We are **not responsible** for any admission, seat allocation, or counseling-related issues.
        - This tool is intended to serve as **guidance only**, not as a final decision-maker.
        - All recommendations are based on **available data** and **algorithms we have developed**.
        - Final allotments depend on official **counseling processes** and **your personal choices**.
        👉 Please use this tool as a **reference**, not as your final choice list. Always verify with official TS EAMCET counseling notifications and guidelines.
        """,
        'benefits_content': """
        ✅ **Why Use This Tool?**
        - Save time by exploring the **most probable and optimal combinations**
        - Make informed decisions based on **rank-wise insights**
        - Avoid common mistakes in web option ordering
        - Use expert patterns to get closer to your dream seat
        """
    }

# ============================================================================
# OPTIMIZED SESSION STATE MANAGEMENT
# ============================================================================


class SessionManager:
    """Manage session state efficiently"""

    @staticmethod
    def initialize():
        """Initialize session state variables once"""
        if 'app_initialized' not in st.session_state:
            # Core app state
            st.session_state.app_initialized = True
            st.session_state.page_configured = False

            # Performance settings
            st.session_state.show_debug_metrics = False
            st.session_state.show_footer_expanded = False

            # Data loading state
            st.session_state.data_loaded = False
            st.session_state.colleges_data = None
            st.session_state.loading_error = None

            # UI state
            st.session_state.current_active_tab = 0
            st.session_state.help_sections_expanded = False

            logger.info("Session state initialized")

    @staticmethod
    def ensure_data_loaded() -> bool:
        """Ensure data is loaded, load if necessary"""
        if not st.session_state.get('data_loaded', False):
            try:
                with st.spinner("🔄 Loading college data..."):
                    st.session_state.colleges_data = load_colleges_data()

                if st.session_state.colleges_data is None:
                    st.session_state.loading_error = "Failed to load college data"
                    return False

                st.session_state.data_loaded = True
                st.session_state.loading_error = None
                return True

            except Exception as e:
                st.session_state.loading_error = f"Error loading data: {str(e)}"
                logger.error(f"Data loading error: {e}")
                return False

        return True

    @staticmethod
    def handle_data_error():
        """Handle data loading errors gracefully"""
        error_msg = st.session_state.get('loading_error')
        if error_msg:
            st.error(f"⚠️ {error_msg}")
            if st.button("🔄 Retry Loading Data"):
                st.session_state.data_loaded = False
                st.session_state.loading_error = None
                st.rerun()

# ============================================================================
# LAZY LOADING MODULE IMPORTS
# ============================================================================


class LazyModuleLoader:
    """Lazy load modules only when needed"""

    _modules = {}

    @classmethod
    def get_module(cls, module_name: str):
        """Get module with lazy loading and caching"""
        if module_name not in cls._modules:
            try:
                if module_name == 'college_predictor':
                    from pagess import college_predictor
                    cls._modules[module_name] = college_predictor
                elif module_name == 'web_options_generator':
                    from pagess import web_options_generator
                    cls._modules[module_name] = web_options_generator
                elif module_name == 'college_specific_generator':
                    from pagess import college_specific_generator
                    cls._modules[module_name] = college_specific_generator
                elif module_name == 'best_specific_generator':
                    from pagess import best_specific_generator
                    cls._modules[module_name] = best_specific_generator
                elif module_name == 'college_branches':
                    from pagess import college_branches
                    cls._modules[module_name] = college_branches
                elif module_name == 'college_search':
                    from pagess import college_search
                    cls._modules[module_name] = college_search
                elif module_name == 'phase_comparison':
                    from pagess import phase_comparison
                    cls._modules[module_name] = phase_comparison
                #     # # Branch Analysis Tab
                #     # with tabs[7]:
                #     #     branch_analysis.render()
                else:
                    logger.warning(f"Unknown module: {module_name}")
                    return None

            except ImportError as e:
                logger.error(f"Failed to import {module_name}: {e}")
                return None

        return cls._modules.get(module_name)

    @classmethod
    def render_module(cls, module_name: str) -> bool:
        """Render module with error handling"""
        module = cls.get_module(module_name)
        if module and hasattr(module, 'render'):
            try:
                module.render()
                return True
            except Exception as e:
                st.error(f"Error rendering {module_name}: {str(e)}")
                logger.error(f"Error in {module_name}: {e}")
                return False
        else:
            st.error(
                f"Module {module_name} not available or missing render method")
            return False

# ============================================================================
# OPTIMIZED UI COMPONENTS
# ============================================================================


def create_optimized_footer():
    """Create footer with cached content and collapsible design"""
    if not st.session_state.get('show_footer_expanded', False):
        with st.expander("👥 About the Developers", expanded=False):
            content = get_static_content()
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(content['footer_tharun'])

            with col2:
                st.markdown(content['footer_goutham'])


def render_support_section():
    """Render optimized support section with cached content"""
    content = get_static_content()

    st.markdown(content['support_message'])
    st.markdown(content['social_links'])

    # Support info
    st.info("""
    💖 **Support This Project**
    To help keep the website running and free for everyone:
    [Support via Razorpay](https://razorpay.me/@your-razorpay-id)
    Link will be updated soon! 😊
    """)

    # Benefits and disclaimer in expandable sections
    col1, col2 = st.columns([1, 1])

    with col1:
        with st.expander("✅ Tool Benefits"):
            st.success(content['benefits_content'])

    with col2:
        with st.expander("⚠️ Important Disclaimer"):
            st.warning(content['disclaimer_content'])


def render_help_tab_optimized():
    """Optimized help tab with better organization"""
    st.subheader("🆘 Help & Information")
    st.markdown("""
        ### 📌 Disclaimer
        This tool is based on the **TS EAMCET 2024 cutoff ranks** published in the TGEAPCET 2024 Last Rank Statement.
        Please note that actual admissions may vary due to:
        - Special category reservations (PH, CAP, NCC, Sports, etc.)
        - Management quotas and spot admissions
        - Student withdrawals and internal college policies
    """)

    content = get_static_content()

    # Main help content
    with st.expander("📖 How to Use This Tool", expanded=True):
        st.markdown(content['help_content'])

        st.markdown("""
    ### 🚀 Detailed Instructions:

    ---

    #### **1. College Predictor Tab**
    - Enter your **TS EAMCET rank**, **gender**, **category**, and **preferred branch**
    - Choose the **counseling phase** (✅ *Final Phase recommended*)
    - Optionally filter by **district**
    - Click **“Predict Colleges”** to see a list of eligible colleges and branches

    ---

    #### **2. Web Options – Branch Specific Generator Tab**
    - Input your **rank**, **gender**, and **category**
    - Select your **preferred branches in priority order**
    - Set a **safety buffer** (e.g., `+300` ranks) to improve your chances
    - Get a **customized, strategic list** of college-branch combinations
    - Download the results as a **CSV** for easier entry in the web options form

    ---

    #### **3. Web Options – College Specific Generator Tab**
    - Enter your **rank**
    - View branches available in **top 20 colleges**
    - Download the list for reference during the web options process

    ---

    #### **4. Web Options – Best Possible Generator Tab**
    - Get **personalized suggestions** for the best possible college-branch matches
    - Uses your **preferences** and **rank** to optimize your admission chances

    ---

    #### **5. College-wise Branches Tab**
    - Select any **college** to view all its **offered branches** and their **closing ranks**
    - Easily compare difficulty levels of departments within a single college
    - View insights on the **top 20 colleges** based on demand and cutoff trends

    ---

    #### **6. College Search by Branch Tab**
    - Search for colleges offering your **preferred branch**
    - Customize the results by **gender** and **category** (or use `N/A` to view all)
    - View additional info like **location**, **district**, and **tuition fees**

    ---

    #### **7. Phase Comparison Tab**
    - Compare how **cutoff ranks** change across **different counseling phases**
    - Helps you decide whether to lock a seat early or wait for later rounds

    ---
    #### 🧰 Web Options Generator – Key Features

    - ✅ **Priority-Based Output**: College-branch options arranged by your chosen branch order.
    - 🎯 **Safety Buffer**: Adds a margin to cutoff ranks for safer predictions.
    - 🏆 **Top College Focus**: Emphasizes top 20 reputed institutions for best outcomes.
    - 🧠 **Smart Filtering**: Balances ambitious choices with realistic chances.
    - 📥 **Download Option**: Export your personalized list for direct use in web counseling.
    """)

    with st.expander("⚠️ Important Disclaimers"):
        st.warning("""
        - This tool uses **TS EAMCET 2024** data for estimation
        - **2025 cutoffs may vary** significantly
        - Always verify with **official TS EAMCET counseling**
        - Special category seats not included in general cutoffs
        """)

    with st.expander("🏆 Top Engineering Colleges(As per our analysis)"):
        top_colleges, top_colleges_males = get_top_colleges_data()

        if top_colleges_males:
            # Show top 15
            for i, college in enumerate(top_colleges_males):
                st.write(
                    f"**{i+1}.** {college.get('name', 'Unknown College')}")
        else:
            st.info("College rankings data not available")

# ============================================================================
# OPTIMIZED TAB RENDERING WITH LAZY LOADING
# ============================================================================


def render_tabs_optimized():
    """Render tabs with optimized lazy loading"""
    tab_configs = [
        ("College Predictor", "college_predictor"),
        ("Web Options Branch-Specific", "web_options_generator"),
        ("Web Options College-Specific", "college_specific_generator"),
        ("Web Options Best Possible", "best_specific_generator"),
        ("College-wise Branches", "college_branches"),
        ("College Search by Branch", "college_search"),
        ("Phase Comparison", "phase_comparison"),
        #  "Branch Analysis",
        ("Help", "help")
    ]

    tabs = st.tabs([config[0] for config in tab_configs])

    # Render tabs with lazy loading
    for i, (tab_name, module_name) in enumerate(tab_configs):
        with tabs[i]:
            if module_name == "help":
                render_help_tab_optimized()
            else:
                # Only load and render if this tab is likely active
                # (Streamlit doesn't provide direct tab state, so we render all but with optimizations)
                success = LazyModuleLoader.render_module(module_name)
                if not success and module_name != "help":
                    st.info(
                        f"The {tab_name} feature is temporarily unavailable. Please try refreshing the page.")

# ============================================================================
# MAIN APPLICATION FUNCTION
# ============================================================================


def main():
    """Optimized main application function"""
    # Start performance monitoring
    perf_metrics = PerformanceMonitor.start_monitoring()

    # Initialize session state
    SessionManager.initialize()

    # Configure page only once
    if not st.session_state.get('page_configured', False):
        st.set_page_config(
            page_title="TS EAMCET 2025 College Predictor",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        st.session_state.page_configured = True

    # Debug settings (only in development)
    # if not os.getenv('STREAMLIT_ENV') == 'production':
    #     with st.sidebar:
    #         st.session_state.show_debug_metrics = st.checkbox(
    #             "Show Debug Metrics")

    # Main title
    st.title("🎓 TS EAMCET 2025 College Predictor")

    # Handle data loading with error recovery
    if not SessionManager.ensure_data_loaded():
        SessionManager.handle_data_error()
        return

    # Render main content
    render_tabs_optimized()

    # Footer and support sections (optimized)
    create_optimized_footer()
    render_support_section()

    # Additional notices
    current_time = get_current_time_ist()

    with st.expander("📋 Important Updates & Information"):
        st.info("""
        **Note**: Due to changes in local and non-local quota policies for TS EAPCET 2025, 
        cutoff ranks may increase significantly compared to previous years. For example, 
        a 1000 rank in 2024 may correspond to a 1500–2000 rank in 2025. 
        Please consider this while selecting your web options. ALL THE BEST! 😊
        """)

        st.caption(f"**Data Source**: TGEAPCET 2024 Last Rank Statement")
        st.caption(f"**Last Updated**: {current_time}")

    # Final message
    st.markdown(
        "# ALL THE BEST FOR YOUR [**NEXTSTEP**](https://nextstep-student-hub.vercel.app/)! 😊🎉")

    # Log performance metrics
    PerformanceMonitor.log_performance(perf_metrics, "Main app render")

# ============================================================================
# ENTRY POINT
# ============================================================================


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Critical application error: {e}")
        st.error("""
        🚨 **Application Error**
        
        Something went wrong! Please try:
        1. Refreshing the page
        2. Clearing your browser cache
        3. Contacting support if the issue persists
        """)

        # Show error details in development
        # if not os.getenv('STREAMLIT_ENV') == 'production':
        #     st.exception(e)

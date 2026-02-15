/**
 * Footer Component
 * Responsive footer using scoped CSS
 */

export function Footer() {
    return (
        <footer id="main-app-footer">
            <div className="container footer-content">
                {/* Left Side: Copyright */}
                <div className="copyright">
                    &copy; 2026 Vet Clinic
                </div>

                {/* Center: System Status
                <div className="status-wrapper">
                    <span className="status-dot"></span>
                    <span>System Status: Operational</span>
                </div> */}

                {/* Right Side: Links */}
                <div className="footer-nav">
                    <a href="#" className="footer-link">Support</a>
                    <a href="#" className="footer-link">Privacy Policy</a>
                    <a href="#" className="footer-link emergency">
                        Emergency Contact
                    </a>
                </div>
            </div>
        </footer>
    );
}

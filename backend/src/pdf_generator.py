from fpdf import FPDF
import os
from datetime import datetime
import io

class PDF(FPDF):
    def __init__(self, user_email="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_email = user_email
        self.add_font("Helvetica", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.add_font("Helvetica", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        self.add_font("Helvetica", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf")

    def header(self):
        # Watermark
        self.set_font("Helvetica", "", 8)
        self.set_text_color(192, 192, 192) # Light grey
        self.text(10, 10, f"Licensed to: {self.user_email} | Inner Bloom Platform")
        self.text(10, 15, f"Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

        # Confidential watermark
        self.set_font("Helvetica", "B", 40)
        self.set_text_color(220, 220, 220) # Very light grey
        self.rotate(45, self.w/2, self.h/2)
        self.text(self.w/2 - self.get_string_width("INNER BLOOM CONFIDENTIAL")/2, self.h/2, "INNER BLOOM CONFIDENTIAL")
        self.rotate(0)
        self.set_text_color(0, 0, 0) # Reset to black

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128) # Grey
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(233, 30, 99) # HexColor("#E91E63")
        self.ln(10)
        self.cell(0, 10, title, 0, 1, "C")
        self.ln(10)

    def chapter_subtitle(self, subtitle):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(99, 102, 241) # HexColor("#6366F1")
        self.ln(5)
        self.cell(0, 10, subtitle, 0, 1, "C")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 12)
        self.set_text_color(0, 0, 0) # Black
        self.multi_cell(0, 8, body)
        self.ln(5)

    def chapter_quote(self, quote):
        self.set_font("Helvetica", "I", 14)
        self.set_text_color(233, 30, 99) # HexColor("#E91E63")
        self.ln(5)
        self.multi_cell(0, 8, quote, align="C")
        self.ln(5)

class PDFGenerator:
    def generate_parenting_guide(self, user_email: str, user_name: str) -> bytes:
        pdf = PDF(user_email=user_email)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Cover page
        pdf.ln(50)
        logo_path = "/home/ubuntu/inner_bloom_logo.png"
        if os.path.exists(logo_path):
            try:
                pdf.image(logo_path, x=pdf.w/2-25, w=50)
                pdf.ln(10)
            except Exception as e:
                print(f"Error adding logo: {e}")
        
        pdf.chapter_title("The Divine Motherhood Blueprint")
        pdf.chapter_subtitle("A Complete Guide to Empowered Parenting")
        pdf.ln(20)
        pdf.chapter_quote(f"Exclusively for: {user_name}")
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Licensed to: {user_email}", 0, 1, "C")

        pdf.add_page()
        pdf.chapter_title("Table of Contents")
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(233, 30, 99) # HexColor("#E91E63")
        pdf.set_text_color(255, 255, 255) # White
        pdf.cell(30, 10, "Chapter", 1, 0, "C", 1)
        pdf.cell(100, 10, "Title", 1, 0, "C", 1)
        pdf.cell(30, 10, "Page", 1, 1, "C", 1)
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(245, 245, 220) # Beige

        toc_data = [
            ["1", "Understanding Your Divine Role as a Mother", "3"],
            ["2", "Toddler Years: Building Foundation with Love", "15"],
            ["3", "Elementary Age: Nurturing Independence", "35"],
            ["4", "Teen Years: Navigating the Storm with Grace", "55"],
            ["5", "Adult Children: Transitioning to Friendship", "75"],
            ["6", "Self-Care for the Divine Mother", "95"],
            ["7", "Building Your Support Network", "115"],
            ["8", "Resources and Tools", "135"]
        ]
        for row in toc_data:
            pdf.cell(30, 10, row[0], 1, 0, "C", 1)
            pdf.cell(100, 10, row[1], 1, 0, "L", 1)
            pdf.cell(30, 10, row[2], 1, 1, "C", 1)

        # Chapter 1
        pdf.add_page()
        pdf.chapter_title("Chapter 1: Understanding Your Divine Role as a Mother")
        pdf.chapter_quote("\"Motherhood is not a burden to be borne, but a divine calling to be embraced.\"")
        chapter1_content = [
            "Welcome to your journey of divine motherhood. As a woman who has chosen to nurture and guide another soul, you have stepped into one of the most sacred roles in existence. This guide will help you navigate the beautiful, challenging, and transformative experience of raising children while maintaining your own identity and purpose.",
            "The concept of \"divine motherhood\" isn\"t about perfection—it\"s about intention, love, and growth. Every mother faces moments of doubt, frustration, and exhaustion. What makes motherhood divine is your commitment to showing up, learning, and loving through it all.",
            "In this chapter, we\"ll explore:",
            "• Understanding your unique parenting style and strengths",
            "• Releasing the myth of the \"perfect mother\"",
            "• Embracing your intuition as your greatest parenting tool",
            "• Creating a vision for the kind of mother you want to be",
            "• Building confidence in your parenting decisions",
            "Remember, dear mother, you were chosen for this child, and this child was chosen for you. Trust in that divine connection as we begin this journey together."
        ]
        for content in chapter1_content:
            pdf.chapter_body(content)

        # Chapter 2
        pdf.add_page()
        pdf.chapter_title("Chapter 2: Toddler Years - Building Foundation with Love")
        pdf.chapter_quote("\"The days are long, but the years are short. Embrace the chaos with grace.\"")
        toddler_content = [
            "The toddler years are often called the most challenging phase of parenting, but they\"re also the most foundational. During this time, you\"re not just managing tantrums and teaching basic skills—you\"re laying the groundwork for your child\"s emotional intelligence, self-worth, and relationship with the world.",
            "Key strategies for toddler parenting:",
            "• Setting loving boundaries that feel safe, not restrictive",
            "• Understanding that tantrums are communication, not manipulation",
            "• Creating routines that provide security and predictability",
            "• Modeling the emotional regulation you want to see",
            "• Celebrating small victories and progress over perfection"
        ]
        for content in toddler_content:
            pdf.chapter_body(content)

        # Chapter 6
        pdf.add_page()
        pdf.chapter_title("Chapter 6: Self-Care for the Divine Mother")
        pdf.chapter_quote("\"You cannot pour from an empty cup. Fill yourself first.\"")
        selfcare_content = [
            "Self-care isn\"t selfish—it\"s essential. As a mother, you\"re constantly giving of yourself, and without intentional replenishment, you\"ll find yourself depleted, resentful, and unable to show up as the mother you want to be.",
            "The Inner Bloom approach to maternal self-care includes:",
            "• Daily micro-moments of joy and peace",
            "• Weekly time for personal interests and hobbies",
            "• Monthly adventures or experiences that feed your soul",
            "• Quarterly retreats or extended self-care periods",
            "• Annual vision-setting and life evaluation",
            "Remember: Taking care of yourself teaches your children that they matter enough to take care of themselves too."
        ]
        for content in selfcare_content:
            pdf.chapter_body(content)

        return pdf.output(dest='S').encode('latin1')

    def generate_empowerment_guide(self, user_email: str, user_name: str) -> bytes:
        pdf = PDF(user_email=user_email)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Cover
        pdf.ln(50)
        logo_path = "/home/ubuntu/inner_bloom_logo.png"
        if os.path.exists(logo_path):
            try:
                pdf.image(logo_path, x=pdf.w/2-25, w=50)
                pdf.ln(10)
            except Exception as e:
                print(f"Error adding logo: {e}")
        pdf.chapter_title("Inner Bloom Empowerment Guide")
        pdf.chapter_subtitle("Unlock Your Limitless Potential")
        pdf.ln(20)
        pdf.chapter_quote(f"Exclusively for: {user_name}")

        pdf.add_page()
        pdf.chapter_title("Chapter 1: Discovering Your Inner Power")
        empowerment_content = [
            "Every woman possesses an infinite well of strength, wisdom, and power. The journey of empowerment isn\"t about gaining something new—it\"s about remembering and reclaiming what was always yours.",
            "In this guide, you\"ll discover:",
            "• How to identify and overcome limiting beliefs",
            "• Techniques for building unshakeable confidence",
            "• Strategies for setting and achieving ambitious goals",
            "• Methods for creating supportive relationships",
            "• Tools for maintaining your power in challenging situations",
            "Your empowerment journey starts now. Are you ready to bloom?"
        ]
        for content in empowerment_content:
            pdf.chapter_body(content)

        return pdf.output(dest='S').encode('latin1')

    def generate_business_guide(self, user_email: str, user_name: str) -> bytes:
        pdf = PDF(user_email=user_email)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Cover
        pdf.ln(50)
        logo_path = "/home/ubuntu/inner_bloom_logo.png"
        if os.path.exists(logo_path):
            try:
                pdf.image(logo_path, x=pdf.w/2-25, w=50)
                pdf.ln(10)
            except Exception as e:
                print(f"Error adding logo: {e}")
        pdf.chapter_title("She-EO Success Blueprint")
        pdf.chapter_subtitle("Build Your Empire with Purpose")
        pdf.ln(20)
        pdf.chapter_quote(f"Exclusively for: {user_name}")

        pdf.add_page()
        pdf.chapter_title("Chapter 1: The Entrepreneurial Mindset")
        business_content = [
            "Being a She-EO isn\"t just about running a business—it\"s about creating impact, building legacy, and designing a life of freedom and fulfillment. This blueprint will guide you through every stage of your entrepreneurial journey.",
            "What you\"ll learn:",
            "• How to identify profitable business opportunities",
            "• Strategies for building a strong personal brand",
            "• Systems for scaling your business sustainably",
            "• Methods for building and leading high-performing teams",
            "• Techniques for maintaining work-life integration",
            "Your business empire awaits. Let\"s build it together."
        ]
        for content in business_content:
            pdf.chapter_body(content)

        return pdf.output(dest='S').encode('latin1')

# Initialize PDF generator
pdf_generator = PDFGenerator()



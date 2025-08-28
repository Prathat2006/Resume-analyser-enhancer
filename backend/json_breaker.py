import json

def extract_experience(json_input):
    """
    Extract the experience field from JSON input
    
    Args:
        json_input: Can be a JSON string, dictionary, or file path
    
    Returns:
        str: The experience value or None if not found
    """
    try:
        # Handle different input types
        if isinstance(json_input, str):
            # Check if it's a file path
            if json_input.endswith('.json'):
                with open(json_input, 'r') as file:
                    data = json.load(file)
            else:
                # Assume it's a JSON string
                data = json.loads(json_input)
        elif isinstance(json_input, dict):
            # Already a dictionary
            data = json_input
        else:
            raise ValueError("Input must be a JSON string, dictionary, or file path")
        
        # Extract experience field
        experience = data.get('experience', None)
        
        if experience is None:
            print("Experience field not found in JSON")
            return {"experience": None}

        return {"experience": experience}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"experience": None}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"experience": None}
    except Exception as e:
        print(f"Error: {e}")
        return {"experience": None}
def extract_education(json_input):
    """
    Extract the education field from JSON input

    Args:
        json_input: Can be a JSON string, dictionary, or file path
    
    Returns:
        str: The education value or None if not found
    """
    try:
        # Handle different input types
        if isinstance(json_input, str):
            # Check if it's a file path
            if json_input.endswith('.json'):
                with open(json_input, 'r') as file:
                    data = json.load(file)
            else:
                # Assume it's a JSON string
                data = json.loads(json_input)
        elif isinstance(json_input, dict):
            # Already a dictionary
            data = json_input
        else:
            raise ValueError("Input must be a JSON string, dictionary, or file path")

        # Extract education field
        education = data.get('education', None)

        if education is None:
            print("Education field not found in JSON")
            return {"education": None}

        return {"education": education}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"education": None}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"education": None}
    except Exception as e:
        print(f"Error: {e}")
        return {"education": None}
def extract_skills(json_input):
    """
    Extract the skills field from JSON input

    Args:
        json_input: Can be a JSON string, dictionary, or file path

    Returns:
        list: The skills value or an empty list if not found
    """
    try:
        # Handle different input types
        if isinstance(json_input, str):
            # Check if it's a file path
            if json_input.endswith('.json'):
                with open(json_input, 'r') as file:
                    data = json.load(file)
            else:
                # Assume it's a JSON string
                data = json.loads(json_input)
        elif isinstance(json_input, dict):
            # Already a dictionary
            data = json_input
        else:
            raise ValueError("Input must be a JSON string, dictionary, or file path")

        # Extract skills field
        skills = data.get('skills', [])

        if not skills:
            print("Skills field not found in JSON")
            return {"skills": []}

        return {"skills": skills}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"skills": []}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"skills": []}
    except Exception as e:
        print(f"Error: {e}")
        return {"skills": []}

def extract_key_skills(json_input):
    """
    Extract the key skills field from JSON input

    Args:
        json_input: Can be a JSON string, dictionary, or file path

    Returns:
        list: The key skills value or an empty list if not found
    """
    try:
        # Handle different input types
        if isinstance(json_input, str):
            # Check if it's a file path
            if json_input.endswith('.json'):
                with open(json_input, 'r') as file:
                    data = json.load(file)
            else:
                # Assume it's a JSON string
                data = json.loads(json_input)
        elif isinstance(json_input, dict):
            # Already a dictionary
            data = json_input
        else:
            raise ValueError("Input must be a JSON string, dictionary, or file path")

        # Extract key skills field
        key_skills = data.get('key_skills', [])

        if not key_skills:
            print("Key skills field not found in JSON")
            return {"key_skills": []}

        return {"key_skills": key_skills}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"key_skills": []}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"key_skills": []}
    except Exception as e:
        print(f"Error: {e}")
        return {"key_skills": []}

def extract_must_skills(json_input):
    """
    Extract the must skills field from JSON input

    Args:
        json_input: Can be a JSON string, dictionary, or file path

    Returns:
        list: The key skills value or an empty list if not found
    """
    try:
        # Handle different input types
        if isinstance(json_input, str):
            # Check if it's a file path
            if json_input.endswith('.json'):
                with open(json_input, 'r') as file:
                    data = json.load(file)
            else:
                # Assume it's a JSON string
                data = json.loads(json_input)
        elif isinstance(json_input, dict):
            # Already a dictionary
            data = json_input
        else:
            raise ValueError("Input must be a JSON string, dictionary, or file path")

        # Extract key skills field
        must_skills = data.get('must_skills', [])

        if not must_skills:
            print("Must skills field not found in JSON")
            return {"must_skills": []}

        return {"must_skills": must_skills}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"must_skills": []}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"must_skills": []}
    except Exception as e:
        print(f"Error: {e}")
        return {"must_skills": []}
    

def extract_github_profile(json_input):
    """
    Extract the GitHub profile field from JSON input

    Args:
        json_input: Can be a JSON string, dictionary, or file path

    Returns:
        list: The GitHub profile value or an empty list if not found
    """
    try:
        # Handle different input types
        if isinstance(json_input, str):
            # Check if it's a file path
            if json_input.endswith('.json'):
                with open(json_input, 'r') as file:
                    data = json.load(file)
            else:
                # Assume it's a JSON string
                data = json.loads(json_input)
        elif isinstance(json_input, dict):
            # Already a dictionary
            data = json_input
        else:
            raise ValueError("Input must be a JSON string, dictionary, or file path")

        # Extract key skills field
        github_profile = data.get('github_profile', [])

        if not github_profile:
            print("GitHub profile field not found in JSON")
            return {"github_profile ": []}

        return {"github_profile": github_profile }

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"github_profile": []}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"github_profile": []}
    except Exception as e:
        print(f"Error: {e}")
        return {"github_profile": []}

# json_input = r"""
# {
#   "title": "Data Science Engineer",
#   "company": "Persistent Careers",
#   "location": "Pune, Bengaluru",
#   "experience": "None",
#   "education": "Education UG: B.Tech/B.E. in Computers PG: M.Tech in Computers",
#   "skills": [
#     "Data Science",
#     "Artificial Intelligence",
#     "Machine Learning",
#     "GEN AI",
#     "LangChain",
#     "LangGraph",
#     "MLOps Architecture Strategy",
#     "Prompt engineering",
#     "MLflow",
#     "Kubeflow",
#     "SageMaker",
#     "Vertex AI",
#     "Docker",
#     "Kubernetes",
#     "AWS",
#     "Azure",
#     "GCP",
#     "Python",
#     "TensorFlow",
#     "PyTorch",
#     "scikit-learn",
#     "CI/CD",
#     "Infrastructure as code",
#     "Automation tools"
#   ],
#   "description": "Job description About Position:   We are conducting an in-person hiring drive for the position of Mlops / Data Science in Pune & Bengaluru on 2nd August 2025.Interview Location is mentioned below: Pune  Persistent Systems, Veda Complex, Rigveda-Yajurveda-Samaveda-Atharvaveda Plot No. 39, Phase I, Rajiv Gandhi Information Technology Park, Hinjawadi, Pune, 411057 Bangalore - Persistent Systems, The Cube at Karle Town Center Rd, DadaMastan Layout, Manayata Tech Park, Nagavara, Bengaluru, Karnataka 560024 We are looking for an experienced and talented Data Science to join our growing data competency team. The ideal candidate will have a strong background in working with GEN AI , ML ,LangChain, LangGraph, Mlops Architecture Strategy, Prompt engineering. You will work closely with our data analysts, engineers, and business teams to ensure optimal performance, scalability, and availability of our data pipelines and analytics. Role: Data Science Job Location: All PSL Location   Experience: 5+ Years Job Type: Full Time Employment What You'll Do:   Design, build, and manage scalable ML model deployment pipelines (CI/CD for ML). Automate model training, validation, monitoring, and retraining workflows. Implement model governance, versioning, and reproducibility best practices. Collaborate with data scientists, engineers, and product teams to operationalize ML solutions. Ensure robust monitoring and performance tuning of deployed models Expertise You'll Bring:   Strong experience with MLOps tools & frameworks (MLflow, Kubeflow, SageMaker, Vertex AI, etc.). Proficient in containerization (Docker, Kubernetes). Good knowledge of cloud platforms (AWS, Azure, or GCP). Expertise in Python and familiarity with ML libraries (TensorFlow, PyTorch, scikit-learn). Solid understanding of CI/CD, infrastructure as code, and automation tools. Benefits: Competitive salary and benefits package Culture focused on talent development with quarterly promotion cycles and company-sponsored higher education and certifications Opportunity to work with cutting-edge technologies Employee engagement initiatives such as project parties, flexible work hours, and Long Service awards Annual health check-ups Insurance coverage: group term life, personal accident, and Mediclaim hospitalization for self, spouse, two children, and parents Inclusive Environment: Persistent Ltd. is dedicated to fostering diversity and inclusion in the workplace. We invite applications from all qualified individuals, including those with disabilities, and regardless of gender or gender preference. We welcome diverse candidates from all backgrounds. We offer hybrid work options and flexible working hours to accommodate various needs and preferences. Our office is equipped with accessible facilities, including adjustable workstations, ergonomic chairs, and assistive technologies to support employees with physical disabilities. If you are a person with disabilities and have specific requirements, please inform us during the application process or at any time during your employment. We are committed to creating an inclusive environment where all employees can thrive. Our company fosters a values-driven and people-centric work environment that enables our employees to: Accelerate growth, both professionally and personally Impact the world in powerful, positive ways, using the latest technologies Enjoy collaborative innovation, with diversity and work-life wellbeing at the core Unlock global opportunities to work and learn with the industry's best Lets unleash your full potential at Persistent \" Persistent is an Equal Opportunity Employer and prohibits discrimination and harassment of any kind. \" Role:  IT Infrastructure Services - Other , Industry Type:  IT Services & Consulting , Department:  IT & Information Security , Employment Type:  Full Time, Permanent Role Category:  IT Infrastructure Services Education UG:  B.Tech/B.E. in Computers PG:  M.Tech in Computers read more Key Skills Skills highlighted with '' are preferred keyskills Data Science Artificial Intelligence Machine Learning",
#   "others": "Role: IT Infrastructure Services - Other, Industry Type: IT Services & Consulting, Department: IT & Information Security, Employment Type: Full Time, Permanent, Role Category: IT Infrastructure Services"
# }
# """
# print(extract_education(json_input))
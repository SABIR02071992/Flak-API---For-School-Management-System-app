# src/middleware/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(allowed_roles):
    """
    कस्टम मिडिलवेयर डेकोरेटर जो यूजर्स के रोल्स को चेक करता है।
    उद्देश्य: मल्टी-टेनेंट रोल बेस्ड एक्सेस कंट्रोल (RBAC)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # 1. सुनिश्चित करें कि रिक्वेस्ट में वैलिड JWT टोकन मौजूद है
            verify_jwt_in_request()
            
            # 2. टोकन के अंदर सेClaims (Data) निकालें
            claims = get_jwt()
            user_role = claims.get("role")

            # 3. रोल वेरिफिकेशन चेक
            # अगर allowed_roles एक लिस्ट है (जैसे ['School Admin', 'Teacher']) तो चेक करें
            if isinstance(allowed_roles, list):
                if user_role not in allowed_roles:
                    return jsonify({
                        "error": f"Access Denied! Your role '{user_role}' is not authorized to view this resource."
                    }), 403
            # अगर सिर्फ एक सिंगल रोल पास किया गया है (जैसे 'super_admin')
            elif user_role != allowed_roles:
                return jsonify({
                    "error": f"Access Denied! Required role: '{allowed_roles}', your role: '{user_role}'"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback if somehow pre-3.9 (though unlikely for a modern Gemini bot)
    ZoneInfo = None

import logging

logger = logging.getLogger(__name__)

def get_current_datetime(timezone: str = None) -> str:
    """Gets the current date and time.
    
    Args:
        timezone: An optional IANA timezone string (e.g., 'Asia/Taipei', 'America/New_York'). 
                  If not provided, it defaults to the local system time.
    """
    try:
        if timezone:
            if ZoneInfo:
                tz = ZoneInfo(timezone)
                dt = datetime.now(tz)
            else:
                return "Error: zoneinfo module is not available on this Python version."
        else:
            # Local time
            dt = datetime.now()
            
        # Format: 2023-10-25 14:30:00 (timezone info)
        return dt.strftime(f"%Y-%m-%d %H:%M:%S %Z").strip()
    except Exception as e:
        logger.error(f"Error fetching datetime for timezone '{timezone}': {e}")
        return f"無法取得 '{timezone}' 的時間: {str(e)}"

def get_tools():
    """Returns a list of callable tools for Gemini."""
    return [get_current_datetime]

from reflector import run_reflector
from config import activities

activity_dict = {
    'Morning Reflection': activities.morning_reflection,
    'End of Day Reflection': activities.end_of_day_reflection,
    'Weekly Reflection': activities.weekly_reflection,
    'Monthly Reflection': activities.monthly_reflection,
    'Acclaim System': activities.acclaim_system,
    'Prismatic System': activities.prismatic_system,
    'Physiology Check': activities.physiology,
    'Wins': activities.wins,
}
run_reflector(activity_dict)

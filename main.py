from reflector.reflector import run_reflector
from reflector import activities

activity_dict = {
    'Morning Reflection': activities.morning_reflection,
    'End of Day Reflection': activities.end_of_day_reflection,
    'Weekly Reflection': activities.weekly_reflection,
    'Monthly Reflection': activities.monthly_reflection,
    'Acclaim System': activities.acclaim_system,
    'Prismatic System': activities.prismatic_system,
    'Physiology Check': activities.physiology_check,
    'Operation SELF': activities.operation_self,
    'Operation Red Dragon': activities.operation_red_dragon,
}


run_reflector(activity_dict)
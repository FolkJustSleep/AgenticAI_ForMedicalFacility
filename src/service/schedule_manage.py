from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Iterable, List, Tuple

from data.postgres import get_connection


DEFAULT_SLOT_MINUTES = 30
SLOT_START_TIMES: List[time] = [
	time(8, 30),
	time(9, 0),
	time(9, 30),
	time(10, 0),
	time(10, 30),
	time(11, 0),
	time(11, 30),
	time(13, 30),
	time(14, 0),
	time(14, 30),
	time(15, 0),
	time(15, 30),
	time(16, 0),
]


def _available_slots(day: datetime.date, booked: Iterable[Tuple[datetime, datetime]], duration_minutes: int) -> List[datetime]:
	"""Return allowed slot starts on the day that are not booked."""

	block = timedelta(minutes=duration_minutes)
	allowed = [datetime.combine(day, slot) for slot in SLOT_START_TIMES]
	free: List[datetime] = []

	for slot_start in allowed:
		slot_end = slot_start + block
		conflict = any(not (slot_end <= start or slot_start >= end) for start, end in booked)
		if not conflict:
			free.append(slot_start)

	return free


def book_doctor_appointment(
	doctor_id: int,
	patient_name: str,
	requested_start: datetime,
	duration_minutes: int = DEFAULT_SLOT_MINUTES,
) -> str:
	"""
	Book an appointment if the slot is free; otherwise return alternatives.

	Expected schema (adjust if your table differs):
		appointments(id serial primary key,
					 doctor_id int not null,
					 patient_name text,
					 appointment_start timestamp,
					 appointment_end timestamp,
					 status text default 'booked')
	"""

	conn = get_connection()
	if not conn:
		return "Unable to connect to the schedule database."

	day = requested_start.date()
	block = timedelta(minutes=duration_minutes)
	requested_end = requested_start + block

	allowed_starts = {datetime.combine(day, slot) for slot in SLOT_START_TIMES}
	if requested_start not in allowed_starts:
		allowed_str = ", ".join(t.strftime("%H:%M") for t in SLOT_START_TIMES)
		return f"Requested time must match available slots: {allowed_str}."

	try:
		with conn:
			with conn.cursor() as cur:
				cur.execute(
					"""
					SELECT appointment_start, appointment_end
					FROM appointments
					WHERE doctor_id = %s
					  AND appointment_start::date = %s
					ORDER BY appointment_start
					""",
					(doctor_id, day),
				)
				booked = [(row[0], row[1]) for row in cur.fetchall()]

				conflict = any(
					not (requested_end <= start or requested_start >= end)
					for start, end in booked
				)

				if not conflict:
					cur.execute(
						"""
						INSERT INTO appointments (doctor_id, patient_name, appointment_start, appointment_end, status)
						VALUES (%s, %s, %s, %s, 'booked')
						RETURNING id
						""",
						(doctor_id, patient_name, requested_start, requested_end),
					)
					appt_id = cur.fetchone()[0]
					return (
						f"Appointment confirmed with doctor {doctor_id} "
						f"on {requested_start.strftime('%Y-%m-%d %H:%M')} (ref #{appt_id})."
					)

				free_slots = _available_slots(day, booked, duration_minutes)
				if free_slots:
					slot_text = ", ".join(slot.strftime("%H:%M") for slot in free_slots)
					return (
						f"Requested time is unavailable. Available times on {day}: "
						f"{slot_text}."
					)

				return (
					f"{day} is fully booked for doctor {doctor_id}. "
					"Please choose another date or doctor."
				)

	except Exception as exc:
		return f"Error while booking appointment: {exc}"
	finally:
		conn.close()

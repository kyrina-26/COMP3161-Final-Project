
# COMP3161 Final Project

This project consists of the backend compoenets of a course management system. It contains both ad database and API that is accessible through a frontend service




## Authors

- [@kyrina-26](https://github.com/kyrina-26/)
- [@DannyB67](https://github.com/DannyB67)
- [@Rungry](https://github.com/Rungry)
- [@Da-Bell](https://github.com/Da-Bell)
- [@wright-elizabeth](https://github.com/wright-elizabeth)

## Tech Stack

**API Framework:** Flask (Python)

**Authentication** JWT

**Database:** MySQL (Raw Queries)

**Data Seeding:** Python (Custom scripts generating bulk SQL INSERT statements)

**Testing:** Postman


## Features

#### User Registration
- A student/lecturer can to create an account.
- A user can register with a userid and password.
- A user can be an admin, lecturer or student.

#### User Login
- A student/lecturer should be able to with credentials.

#### Course Creation
- Admins can create courses.
- Course creation is restricted to admins only.

#### Course Retrieval
- Retrieve all courses in the system.
- Retrieve courses for a particular student.
- Retrieve courses taught by a particular lecturer.

#### Course Registration
- Students are able to regsiter for courses.
- Lecturer assignment is limited to 1 lecturer per course.

#### Member Retrieval
- Return members of a particular course.

#### Calendar Event Retrieval
- Return all calendar events for a particular course.
- Return all calendar events for a particular date for a particular
student.

#### Calendar Event Creation
- Create calendar events for a course.

#### Forums
- Create forums for a particular course.
- Retrieve all forums for a particular course.

#### Discussion Threads
-  Retrieve all the discussion threads for a particular forum.
- Add a new discussion thread to a forum. Each discussion thread has a title and the post that started the thread.
- Users can reply to a thread and replies can have replies. 

#### Course Content Management
- Lecturers can add content to a course. Content consists of files, links and slides.
- Content is grouped by section.
- Retrieve all content for a particular course.

#### Assignment Handling
- Students can submit assignments.
- Lecturers can assign grades to a specific student for an ssignment.
- Each grade a student receives goes towards a final average.

#### Reports
The system will generate reports according to the following criteria:

- All courses that have 50 or more students
- All students that do 5 or more courses.
- All lecturers that teach 3 or more courses.
- The 10 most enrolled courses.
- The top 10 students with the highest overall averages.








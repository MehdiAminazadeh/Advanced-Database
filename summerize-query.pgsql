WITH RECURSIVE t(LID, matrnr) AS (
    SELECT exam.LID, exam.matrnr 
    FROM exam
    WHERE exam.grade = (SELECT min(grade) FROM exam)
    UNION ALL
    SELECT prerequisites.required, t.matrnr 
    FROM t
    JOIN prerequisites ON t.LID = prerequisites.lecture
)
SELECT
    s.name,
    x.cnt
FROM
    students s
LEFT OUTER JOIN
    (SELECT count(*) cnt, matrnr FROM t GROUP BY matrnr) x ON s.matrnr = x.matrnr;

/*
The original query performs a three-way nested loop join and an aggregation for each student, which is inefficient
We just run the recursive subquery once and return the "matrnr" with the count
and on the first steps, while we need the matrnr, so we eliminate the "students" table

what is happens in the LEFT OUTER JOIN is that we included every student even if they don't match in the subquery 
results

recursive t : it starts with the minimum grade and add the prerequisities lectures for the returned exams

*/


--- original query 

SELECT P.playerId
FROM Player P, Game G
WHERE P.playerId = G.playerId
GROUP BY P.playerId
HAVING COUNT(G.id) > 10

--- solution

SELECT P.playerId
FROM Player P
INNER JOIN Game G ON P.playerId = G.playerId
GROUP BY P.playerId
HAVING COUNT(G.id) > 10

/*
find players who have participated in more than 10 games. 
An INNER JOIN is sufficient because we are only interested in players who have played games. 
If a player has not played any games, 
they will not contribute to the result set, and their absence does not affect the correctness of the query
 */


 --- original

SELECT P.name, COUNT(G.name)
FROM Player P
LEFT OUTER JOIN Game G
ON P.playerId = G.playerId
GROUP BY P.name

--- solution

SELECT P.name, COUNT(G.playerId)
FROM Player P
LEFT OUTER JOIN Game G
ON P.playerId = G.playerId
GROUP BY P.name


/*
Selecting optimal plans for two relations
the minimal costs for pairwise joins:

R1 ⋈ R2 = 60
R2 ⋈ R3 = 10 (lowest cost)
R3 ⋈ R4 = 36 

we need these for further joins to relations
(R2⋈R3)⋈R4 = 28 (lowest cost) : R2, R3, R4
(R2⋈R3)⋈R1 = 70 : R1, R2, R3
(R3⋈R4)⋈R1 = 1476 (highest) which is not optimal

optimal plans for all relations of R1, R2, R3, R4

Plan 1: Start with (R2⋈R3)⋈R4 then join with R1:
    Cost = 28 + 40 * 18 * 0.15 = 28 + 108 = 136

plan 2: start with (R2⋈R3)⋈R1 then join with R4:
    Cost = 70  + 60 * 30 * 0.06 = 70 + 108 = 178

plan 3: start with (R3⋈R4)⋈R1 then join with R2:
    Cost = 1476 + 30 * 40 * 0.05 = 1476 +60 = 1536

from the above plans we come to plan 1 which hast the most minimal cost
Cost = 136    the bushy tree of R1 ⋈ ((R3 ⋈ R4) ⋈ R2)
 */

SELECT date, count(USER) AS users
   FROM
     (SELECT min(date) AS date,
             account AS USER
      FROM
        (SELECT date_trunc('week', min(evt_block_time)) AS date,
                lad AS account
         FROM maker."SaiTub_evt_LogNewCup"
         GROUP BY 2
         UNION SELECT date_trunc('week', min(block_time)) AS date,
                      borrower
         FROM lending."borrow"
         WHERE project='MakerDAO'
         GROUP BY 2) AS a
      GROUP BY 2) AS b
   GROUP BY 1

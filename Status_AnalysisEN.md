# Preliminary analysis of selected status files for wind turbine SCADA datasets
## Kelmarsh
We have looked into first dataset that consisted of six wind turbines 
from Kelmarsh wind farm located in the UK. Status information for wind turbines 
corresponds with those that we have taken account into during general analysis.
<br>
Data was collected from 1st of January to 30th of June 2021. Timestamps are more irregular,
since this dataset contains information about error and status codes that might
occur more randomly.

### Results

The following results were obtained during the first analysis of the data: <br>

| | Turbine 01          | Turbine 02          | Turbine 03          | Turbine 04          | Turbine 05           | Turbine 06          |
| --- |---------------------|---------------------|---------------------|---------------------|----------------------|---------------------|
| **Columns (variables)**  | 9                   | 9                   | 9                   | 9                   | 9                    | 9                   |
| **Datapoints** | 28565               | 21390               | 32399               | 30871               | 30095                | 37159               |
| **First timestamp** | 2020-12-31 04:43:55 | 2020-12-31 06:14:21 | 2021-01-01 09:47:28 | 2020-12-28 09:23:24 | 2020-12-31 06:02:04  | 2020-06-07 12:20:51 |
| **Last timestamp** | 2021-06-30 23:50:37 | 2021-06-30 18:28:41 | 2021-06-30 19:12:49 | 2021-06-30 19:21:45 | 2021-06-30 22:54:51  | 2021-06-30 23:17:34 
| **Missing values** | 17191              |  13359              | 20341              | 18584              | 18145               | 22421              |

We have noticed that number of missing values is significant. After taking a closer look into
the data we have noticed some correlations between data points.
<br>
1. <b>Timestamps and duration <br> </b>
    There were 3 values that described position in time for the windturbine. Timestamp start, timestamp end
    and duration. Timestamp start is never missing, but duration is tightly coupled to Timestamp end. If we have Timestamp end
    we also have duration, thus in reality we have less missing values.
2. <b> Status, codes and messages  <br></b> 
    Those described type, code and message of a status of a turbine and were never missing.
3. <b>Comment</b> <br>
    This row was always empty, so we do not have to pay attention to it.
4. <b>Service contract category and IEC category</b> <br>
    Number of missing service contract category is significant, but IEC category is almost always present.

### Real number of missing values
Since we have eliminated some missing values from the analysis, we could calculate real number of missing values:

| | Turbine 01 | Turbine 02 | Turbine 03          | Turbine 04          | Turbine 05           | Turbine 06          |
| --- |------------|------------|---------------------|---------------------|----------------------|---------------------|
| **Datapoints** | 28565      | 21390      | 32399               | 30871               | 30095                | 37159               |
| **Missing values** | 17191      | 13359      | 20341              | 18584              | 18145               | 22421              |
| **Missing values without irrelevant data** | 7881       | 6292       | 9588| 8540| 8322|10398 |


We can see that this number is halved compared to previous result.

## Penmanshiel
Situation for this British wind farm located in Penmanshiel is similar to Kelmarsh. This time 5 different turbines were
taken into account. Irrelevant or reduntand data was also 
calculated to present following result:

### Results
|                                            | Turbine 01 | Turbine 02 | Turbine 03 | Turbine 04 | Turbine 05 |
|--------------------------------------------| --- |--- | --- | --- | --- |
| **Columns (variables)**                    | 9  | 9 | 9 | 9 | 9 |
| **Datapoints**                             | 31352 | 26157 | 32117 | 31486 | 26687 | 
| **First timestamp**                        | 2021-01-01 09:47:45 | 2021-01-01 09:47:44 | 2021-01-01 09:47:51 | 2021-01-01 09:47:51 | 2020-12-21 17:08:09 |
| **Last timestamp**                         | 2021-06-30 23:06:10 | 2021-06-30 22:36:29 | 2021-06-30 22:35:17 | 2021-06-30 22:41:56 | 2021-06-30 22:41:15 |
| **Missing values**                         | 19633 | 16350 | 19651 | 19751 | 16738 |
| **Missing values without irrelevant data** | 9099       | 7618       | 9105| 9148| 7776|

We can see that number of missing values halved after eliminating coupled and irrelevant data. 
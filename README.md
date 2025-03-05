# dbt_ragster

This is a [Dagster](https://dagster.io/) project scaffolded with [`dagster project scaffold`](https://docs.dagster.io/getting-started/create-new-project).


## My Goals
Hi, Hello anyone other than myself that comes along this project! My plan for this entire project is to turn it into something that I can explore numerous ideas and topics around. This includes:
- Improving data modelling
- Working with a scheduler
- Improving data engineering skills
- Working with dbt
- Improving deep learning understanding

Now, my day-to-day work is in data science, so why would a data scientist be concerned with data modelling, scheduling,.....? It is my own persional opinion that as a Data Scientist, we should be familiar with all of the workings of a pipeline. This is why I have such lofty goals for this project and what I hope to do.

DBT TO ADDS:
use the env_vars function for the profiles.yml, add more models to the project (think about what transformations I may want), create a macro just because why not, potentially use snapshots in the data.

For the models, think of something that I may want updated every time the project runs (eg, time series stuff) and go from there

### To complete:
These are things that I want to complete for the project:
- [x] Add and schedule dbt runs to the project. Schedule all assets
- [ ] Add grafana for visualization of data
- [ ] Use LLM to get emotion in reddit comments
- [ ] Use the emotion classified from previous step, perform transfer learning on model (This is a bad idea, but I want to use my own data for this, and labelling will be a nightmare)
- [ ] Add LLM model training/retraining to the asset execution

### Nice to Haves:
Some things I can look to add to the project once I have the large majority above done:
- [ ] Data validation with pydantic dataclasses
- [ ] Storing dump of data from current run to S3 (Minio most likely)
- [ ] others?

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.
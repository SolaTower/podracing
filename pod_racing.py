import logging

logger = logging.getLogger()
i = lap = 0
last = target = None


class Checkpoint:

    def __init__(self, x_, y_, dist_, angle_, name_):
        self.x = x_
        self.y = y_
        self.dist = dist_
        self.angle = angle_
        self.name = name_
        self.lap = 1

    @property
    def coord(self):
        return self.x, self.y

    def __str__(self):
        return f"{self.name}: {self.x}:{self.y}"


class Race:
    def __init__(self):
        self.checkpoints = []
        self.size = 0
        self.mapped = False

    def add(self, x_, y_, dist_, angle_):
        self.checkpoints.append(Checkpoint(x_=x_, y_=y_, dist_=dist_, angle_=angle_, name_=self.size))
        self.size += 1

    def prev(self, checkpoint: Checkpoint):
        return self.checkpoints[self.checkpoints.index(checkpoint) - 1] if self.checkpoints.index(checkpoint) else None

    def next(self, checkpoint: Checkpoint):
        return self.checkpoints[self.checkpoints.index(checkpoint) + 1] if checkpoint != self.checkpoints[-1] else None

    def get_furthest_for_boost(self):
        if self.checkpoints[-1].dist > 5000:
            return self.checkpoints[-1]
        return max(self.checkpoints, key=lambda data: data.dist)

    def checkpoint_is_registered(self, x, y):
        return any(checkpoint for checkpoint in self.checkpoints if checkpoint.coord == (x, y))

    def is_mapped(self):
        return self.mapped

    def check_race_mapping(self, x, y):
        logger.error(self.checkpoints[-1].coord)
        logger.error((x, y))
        if self.checkpoints[-1].coord != (x, y):
            self.mapped = True


class Pod:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.checkpoint_x = 0
        self.checkpoint_y = 0
        self.checkpoint_dist = 0
        self.checkpoint_angle = 0
        self.opponent_x = 0
        self.opponent_y = 0
        self.should_boost = False
        self.race = Race()
        self.boost_count = 1
        self.last_checkpoint = 0,0

    def tick(self):
        self.x, self.y, self.checkpoint_x, self.checkpoint_y, self.checkpoint_dist, self.checkpoint_angle = [
            int(data) for data in input().split()]
        self.opponent_x, self.opponent_y = [int(data) for data in input().split()]
        if not self.race.is_mapped() and not self.race.checkpoint_is_registered(self.checkpoint_x, self.checkpoint_y):
            self.race.add(
                self.checkpoint_x,
                self.checkpoint_y,
                self.checkpoint_dist,
                self.checkpoint_angle
            )
        self.race.check_race_mapping(self.checkpoint_x, self.checkpoint_y)
        if self.race.is_mapped():
            self.find_next_boost()
        self.last_checkpoint = self.checkpoint_x, self.checkpoint_y  #fixme

    def get_trust(self):
        if (
                self.should_boost and self.boost_count and abs(self.checkpoint_angle) <= 5 and (
                    (self.should_boost == (self.checkpoint_x, self.checkpoint_y) and
                     self.should_boost != self.race.checkpoints[-1].coord)
                    or
                    (self.should_boost == (self.checkpoint_x, self.checkpoint_y) and
                     self.should_boost == self.race.checkpoints[-1].coord and self.race.lap == 3)
                )
        ):
            self.boost_count -= 1
            next_trust = "BOOST"
        else:
            next_trust = int((190 - abs(self.checkpoint_angle)) / 180 * 100)
            if next_trust > 90:
                next_trust = 100
            elif next_trust < 40:
                next_trust = 60
            if self.checkpoint_dist < 2000:
                next_trust = 40
            next_trust = str(next_trust)
        return next_trust

    def find_next_boost(self):
        if self.race.checkpoints[-1].dist > 5000:
            if self.boost_count == 1 and self.lap #fixme
            return self.checkpoints[-1]
        return max(self.checkpoints, key=lambda data: data.dist)

pod = Pod()
while True:
    try:
        pod.tick()
        print(str(pod.checkpoint_x) + " " + str(pod.checkpoint_y) + " " + pod.get_trust())
    except Exception as exc:
        from traceback import format_exc
        logger.error(format_exc())
        raise

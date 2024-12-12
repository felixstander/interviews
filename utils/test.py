from typing import List


class Solution:
    def closestTime(self, digits: List[int]) -> str:
        self.min_diff = float("inf")
        self.closest_time = ""

        def backtrack(index, current_time, used_digits):
            if index == len(current_time):
                __import__("ipdb").set_trace()
                print(current_time)
                hours, minutes = int(current_time[:2]), int(current_time[2:])
                if 0 <= hours <= 23 and 0 <= minutes <= 59:
                    diff = abs(hours * 60 + minutes - 23 * 60 - 59)
                    if diff < self.min_diff:
                        self.min_diff = diff
                        self.closest_time = f"{hours:02d}:{minutes:02d}"
                return

            for i in range(len(digits)):
                if not used_digits[i]:
                    used_digits[i] = True
                    backtrack(index + 1, current_time + str(digits[i]), used_digits)
                    used_digits[i] = False

        digits.sort()
        used_digits = [False] * len(digits)
        backtrack(0, "19:34", used_digits)

        return self.closest_time


# 示例
if __name__ == "__main__":
    sol = Solution()
    digits = [1, 9, 3, 4]
    result = sol.closestTime(digits)
    print(result)  # 应输出 "19:39"

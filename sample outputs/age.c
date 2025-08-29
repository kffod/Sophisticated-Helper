#include <time.h>
#include <stdio.h>

int getAge(int year, int month, int day) {
    time_t now;
    struct tm *ltm;
    time(&now);
    ltm = localtime(&now);
    int currentYear = 1900 + ltm->tm_year;
    int currentMonth = 1 + ltm->tm_mon;
    int currentDay = ltm->tm_mday;
    int age = currentYear - year;
    if (currentMonth < month || (currentMonth == month && currentDay < day)) {
        age--;
    }
    return age;
}

int main() {
    int year, month, day;
    printf("Enter your birth year: ");
    scanf("%d", &year);
    printf("Enter your birth month (1-12): ");
    scanf("%d", &month);
    printf("Enter your birth day: ");
    scanf("%d", &day);
    if(year > currentYear || month < 1 || month > 12 || day < 1 || day > 31){
        printf("Invalid input\n");
        return 1;
    }
    int age = getAge(year, month, day);
    printf("Your age is: %d\n", age);
    return 0;
}